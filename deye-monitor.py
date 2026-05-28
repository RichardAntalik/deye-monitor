#!/usr/bin/env python3
import os
import sys

_script_dir = os.path.dirname(os.path.abspath(__file__))
_venv = os.path.join(_script_dir, 'venv')
if os.path.isdir(_venv):
    for entry in os.listdir(os.path.join(_venv, 'lib')):
        sp = os.path.join(_venv, 'lib', entry, 'site-packages')
        if os.path.isdir(sp):
            sys.path.insert(0, sp)
            break

import argparse
import json
import signal
import sqlite3
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

from pysolarmanv5 import PySolarmanV5
from pysolarmanv5.pysolarmanv5 import NoSocketAvailableError
from pymodbus.exceptions import ModbusException
from umodbus.exceptions import ModbusError as UmodbusError
import struct

# ─── Configuration ──────────────────────────────────────────────────────────

INVERTER_IP = "192.168.1.2"
INVERTER_PORT = 8899
INVERTER_SN = 3168400438
MB_SLAVE_ID = 1
HTTP_HOST = "0.0.0.0"
HTTP_PORT = 80

# ─── Modbus Register Definitions ────────────────────────────────────────────

REGISTER_GROUPS = {
    "Solar PV 1": [
        (109, "PV1 Voltage", "V", 0.1, 0),
        (110, "PV1 Current", "A", 0.1, 0),
        (186, "PV1 Power", "W", 1, 15),
    ],
    "Solar PV 2": [
        (111, "PV2 Voltage", "V", 0.1, 0),
        (112, "PV2 Current", "A", 0.1, 0),
        (187, "PV2 Power", "W", 1, 15),
    ],
    "Inverter": [
        (154, "Inverter Voltage", "V", 0.1, 0),
        (164, "Inverter Current", "A", 0.01, 0),
        (175, "Inverter Power", "W", 1, 15),
        (193, "Inverter Freq", "Hz", 0.01, 0),
    ],
    "Grid": [
        (79, "Grid Frequency", "Hz", 0.01, 0),
        (150, "Grid Voltage", "V", 0.1, 0),
        (160, "Grid Current L", "A", 0.01, 0),
        (161, "Grid Current N", "A", 0.01, 0),
        (169, "Grid Power", "W", 1, 15),
        (172, "Grid CT Power", "W", 1, 15),
    ],
    "Load": [
        (176, "Load Power L1", "W", 1, 15),
        (178, "Load Power Total", "W", 1, 15),
        (157, "Load Voltage L1", "V", 0.1, 0),
        (179, "Load Current L1", "A", 0.01, 15),
        (192, "Load Frequency", "Hz", 0.01, 0),
    ],
    "Battery": [
        (182, "Battery Temp", "°C", 0.1, 0),
        (183, "Battery Voltage", "V", 0.01, 0),
        (184, "Battery SOC", "%", 1, 0),
        (190, "Battery Power", "W", 1, 15),
        (191, "Battery Current", "A", 0.01, 15),
        (314, "Batt Charge Limit", "A", 1, 15),
        (315, "Batt Discharge Limit", "A", 1, 15),
    ],
    "AUX / Generator": [
        (166, "AUX Power", "W", 1, 15),
        (181, "AUX Voltage", "V", 0.1, 0),
        (196, "AUX Frequency", "Hz", 0.1, 0),
    ],
}

ALL_REGISTERS = []
for group_regs in REGISTER_GROUPS.values():
    ALL_REGISTERS.extend(group_regs)
ALL_REGISTERS.sort(key=lambda r: r[0])


# ─── Helpers ────────────────────────────────────────────────────────────────

_last_error_time = 0
_error_count = 0

def read_chunk(solarman, start_addr, count):
    global _last_error_time, _error_count
    try:
        raw = solarman.read_holding_registers(start_addr, count)
        return list(raw)
    except (ModbusException, UmodbusError):
        _error_count += 1
        now = time.time()
        if now - _last_error_time > 60:
            print(f"  Modbus error at addr {start_addr} (count={_error_count})")
            _last_error_time = now
            _error_count = 0
        return None
    except struct.error:
        _error_count += 1
        now = time.time()
        if now - _last_error_time > 60:
            print(f"  Struct error at addr {start_addr} (count={_error_count})")
            _last_error_time = now
            _error_count = 0
        return None
    except Exception as e:
        _error_count += 1
        now = time.time()
        if now - _last_error_time > 60:
            print(f"  Read error at addr {start_addr}: {e}")
            _last_error_time = now
            _error_count = 0
        return None


def read_all(solarman):
    if not ALL_REGISTERS:
        return {}

    MAX_CHUNK = 50
    values = {}
    all_ok = True

    i = 0
    while i < len(ALL_REGISTERS):
        start = ALL_REGISTERS[i][0]
        max_end_addr = start + MAX_CHUNK - 1
        chunk_end = i + 1
        for j in range(i + 1, len(ALL_REGISTERS)):
            if ALL_REGISTERS[j][0] <= max_end_addr:
                chunk_end = j + 1
            else:
                break
        chunk = ALL_REGISTERS[i:chunk_end]
        end = chunk[-1][0]
        count = end - start + 1

        raw = read_chunk(solarman, start, count)
        if raw is None:
            all_ok = False
            i = chunk_end
            continue

        for addr, name, unit, scale, sign_bit in chunk:
            idx = addr - start
            if idx < len(raw):
                val = raw[idx]
                if sign_bit and val >= (1 << sign_bit):
                    val = val - (1 << 16)
                if addr == 182:
                    val = (val - 1000) * scale
                else:
                    val = val * scale
                values[name] = round(val, 2)
            else:
                values[name] = None
        i = chunk_end

    return values if all_ok else None


def format_power(watts):
    if watts is None:
        return "N/A"
    if abs(watts) >= 1000:
        return f"{watts/1000:+.2f} kW"
    return f"{watts:+.0f} W"


def print_readings(values):
    for group_name, regs in REGISTER_GROUPS.items():
        for addr, name, unit, scale, sign_bit in regs:
            val = values.get(name)
            if val is None:
                print(f"{name}  ---")
            elif unit == "W":
                print(f"{name}  {format_power(val)}")
            else:
                print(f"{name}  {val:.2f} {unit}")
    print()


# ─── SQLite Logger ──────────────────────────────────────────────────────────

_db_conn = None
_db_write_interval = 60
_reading_buffer = []
_buffer_lock = threading.Lock()
_db_stop_event = threading.Event()


def _create_db(db_path):
    global _db_conn
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    _db_conn = sqlite3.connect(db_path, check_same_thread=False)
    _db_conn.execute("PRAGMA journal_mode=WAL")
    col_defs = []
    for _, name, _, _, _ in ALL_REGISTERS:
        col_defs.append(f'`{name}` REAL')
    _db_conn.execute(f"""CREATE TABLE IF NOT EXISTS readings (
        timestamp INTEGER PRIMARY KEY,
        {', '.join(col_defs)}
    )""")
    _db_conn.commit()


def _average_readings(readings):
    result = {}
    for _, name, _, _, _ in ALL_REGISTERS:
        vals = [r.get(name) for r in readings if r.get(name) is not None]
        if vals:
            result[name] = round(sum(vals) / len(vals), 2)
        else:
            result[name] = None
    return result


def _db_writer(db_path, interval):
    _create_db(db_path)
    while not _db_stop_event.is_set():
        _db_stop_event.wait(interval)
        if _db_stop_event.is_set():
            break
        with _buffer_lock:
            batch = _reading_buffer[:]
            _reading_buffer.clear()
        if not batch:
            continue
        avg = _average_readings(batch)
        ts = int(time.time())
        try:
            cols = []
            vals = []
            for _, name, _, _, _ in ALL_REGISTERS:
                cols.append(f'`{name}`')
                v = avg.get(name)
                vals.append('NULL' if v is None else str(v))
            sql = f"INSERT OR REPLACE INTO readings (timestamp, {', '.join(cols)}) VALUES ({ts}, {', '.join(vals)})"
            _db_conn.execute(sql)
            _db_conn.commit()
        except Exception as e:
            print(f"  DB write error: {e}")


def _flush_last_batch():
    with _buffer_lock:
        batch = _reading_buffer[:]
        _reading_buffer.clear()
    if not batch:
        return
    avg = _average_readings(batch)
    ts = int(time.time())
    try:
        cols = []
        vals = []
        for _, name, _, _, _ in ALL_REGISTERS:
            cols.append(f'`{name}`')
            v = avg.get(name)
            vals.append('NULL' if v is None else str(v))
        sql = f"INSERT OR REPLACE INTO readings (timestamp, {', '.join(cols)}) VALUES ({ts}, {', '.join(vals)})"
        _db_conn.execute(sql)
        _db_conn.commit()
        print(f"  Final batch written to DB: {len(batch)} readings")
    except Exception as e:
        print(f"  DB write error on shutdown: {e}")


def signal_handler(signum, frame):
    print("\n\nStopped.")
    if _db_conn:
        _db_stop_event.set()
        _flush_last_batch()
        _db_conn.close()
    sys.exit(0)


# ─── HTTP Handler ───────────────────────────────────────────────────────────

_script_dir = os.path.dirname(os.path.abspath(__file__))
_dashboard_path = os.path.join(_script_dir, 'dashboard.html')

solarman = None
latest_data = None
data_lock = threading.Lock()


class PVHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/PV':
            with data_lock:
                payload = json.dumps(latest_data or {})
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(payload.encode())
        elif self.path.startswith('/api/readings'):
            self._handle_readings_api()
        elif self.path == '/':
            with open(_dashboard_path, 'r') as f:
                html = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass

    def _handle_readings_api(self):
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        start = params.get('start', [None])[0]
        end = params.get('end', [None])[0]
        if not start or not end:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "start and end parameters required"}).encode())
            return
        start = int(start)
        end = int(end)
        try:
            col_names_str = ', '.join([f'`{r[1]}`' for r in ALL_REGISTERS])
            sql = f"SELECT timestamp, {col_names_str} FROM readings WHERE timestamp >= ? AND timestamp <= ? ORDER BY timestamp"
            cur = _db_conn.cursor()
            cur.execute(sql, (start, end))
            rows = cur.fetchall()
            if not rows:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps([]).encode())
                return
            col_names = [desc[0] for desc in cur.description]
            result = []
            for row in rows:
                obj = {}
                for i, name in enumerate(col_names):
                    val = row[i]
                    if name == 'timestamp':
                        obj[name] = val
                    else:
                        obj[name] = float(val) if val is not None else None
                result.append(obj)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())


def data_poller(args):
    global solarman, latest_data
    while True:
        try:
            if solarman is None:
                try:
                    solarman = PySolarmanV5(
                        args.host,
                        INVERTER_SN,
                        port=args.port,
                        mb_slave_id=MB_SLAVE_ID,
                        timeout=5,
                        retry_count=3,
                    )
                    solarman.read_holding_registers(79, 1)
                    print("Reconnected to inverter.")
                except Exception as e:
                    print(f"Reconnect failed: {e}")
                    solarman = None
                    time.sleep(5)
                    continue
            vals = read_all(solarman)
            if vals:
                with data_lock:
                    latest_data = vals
                with _buffer_lock:
                    _reading_buffer.append(vals)
        except Exception as e:
            print(f"Poller error: {e}")
            solarman = None
        time.sleep(3)


# ─── Main ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Deye SUN-6k-SG03LP1-EU inverter monitor with HTTP dashboard"
    )
    parser.add_argument("--host", default=INVERTER_IP,
                        help=f"Inverter IP (default: {INVERTER_IP})")
    parser.add_argument("--port", type=int, default=INVERTER_PORT,
                        help=f"Modbus port (default: {INVERTER_PORT})")
    parser.add_argument("--interval", type=int, default=3,
                        help="Polling interval in seconds (default: 3)")
    parser.add_argument("--db", default=None,
                        help="SQLite database file path for logging")
    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal_handler)

    global solarman
    try:
        solarman = PySolarmanV5(
            args.host,
            INVERTER_SN,
            port=args.port,
            mb_slave_id=MB_SLAVE_ID,
            timeout=5,
            retry_count=3,
        )
    except NoSocketAvailableError:
        print(f"ERROR: Cannot create socket to inverter at {args.host}:{args.port}")
        print(f"  Check that the inverter is powered on and connected to the network.")
        print(f"  Use --host to specify the correct IP address.")
        sys.exit(1)

    try:
        solarman.read_holding_registers(79, 1)
    except NoSocketAvailableError:
        print(f"ERROR: Cannot reach inverter at {args.host}:{args.port}")
        print(f"  The inverter may be offline, on a different subnet, or blocking the connection.")
        print(f"  Use --host to specify the correct IP address.")
        sys.exit(1)
    except ModbusException as e:
        print(f"ERROR: Modbus communication failed with inverter at {args.host}:{args.port}")
        print(f"  {e}")
        print(f"  Check the Modbus port ({args.port}), slave ID ({MB_SLAVE_ID}), and network connection.")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Cannot connect to inverter at {args.host}:{args.port}: {e}")
        sys.exit(1)

    # Start data poller thread
    poller = threading.Thread(target=data_poller, args=(args,), daemon=True)
    poller.start()

    # Start DB writer thread
    db_writer = None
    if args.db:
        db_writer = threading.Thread(
            target=_db_writer, args=(args.db, _db_write_interval), daemon=True
        )
        db_writer.start()
        print(f"SQLite logging enabled: {args.db}")

    # Start HTTP server
    try:
        server = HTTPServer((HTTP_HOST, HTTP_PORT), PVHandler)
    except PermissionError:
        print(f"ERROR: Permission denied binding to port {HTTP_PORT}.")
        print(f"  Port 80 requires root privileges. Run with sudo:")
        print(f"    sudo python3 deye-monitor.py")
        print(f"  Or set the capability on the Python binary:")
        print(f"    sudo setcap 'cap_net_bind_service=+ep' $(readlink -f $(which python3))")
        print(f"  Or use --port to specify a different port (e.g. --port 8080).")
        sys.exit(1)
    except OSError as e:
        print(f"ERROR: Cannot bind to port {HTTP_PORT}: {e}")
        print(f"  Another service may already be using this port.")
        print(f"  Use --port to specify a different port.")
        sys.exit(1)

    print(f"Dashboard: http://<this-host>:{HTTP_PORT}")
    print(f"API:       http://<this-host>:{HTTP_PORT}/PV")
    print("Press Ctrl+C to stop.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()
        solarman.disconnect()


if __name__ == "__main__":
    main()
