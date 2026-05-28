import os
import struct
import threading
import time
import sqlite3

from pysolarmanv5 import PySolarmanV5
from pysolarmanv5.pysolarmanv5 import NoSocketAvailableError
from pymodbus.exceptions import ModbusException
from umodbus.exceptions import ModbusError as UmodbusError

# ─── Configuration ──────────────────────────────────────────────────────────

INVERTER_IP = "192.168.1.2"
INVERTER_PORT = 8899
INVERTER_SN = 3168400438
MB_SLAVE_ID = 1
DEFAULT_SN = INVERTER_SN

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


# ─── Inverter Class ─────────────────────────────────────────────────────────

class Inverter:
    def __init__(self, host=None, port=None, sn=None, db_path=None, interval=3):
        self.host = host or INVERTER_IP
        self.port = port or INVERTER_PORT
        self.sn = sn or DEFAULT_SN
        self.db_path = db_path
        self.interval = interval
        self.solarman = None
        self.latest_data = None
        self.data_lock = threading.Lock()
        self._poller = None
        self._db_writer_thread = None

    def connect(self):
        try:
            self.solarman = PySolarmanV5(
                self.host,
                self.sn,
                port=self.port,
                mb_slave_id=MB_SLAVE_ID,
                timeout=5,
                retry_count=3,
            )
            self.solarman.read_holding_registers(79, 1)
            print("Connected to inverter.")
        except NoSocketAvailableError:
            print(f"ERROR: Cannot create socket to inverter at {self.host}:{self.port}")
            print(f"  Check that the inverter is powered on and connected to the network.")
            raise
        except Exception as e:
            print(f"ERROR: Cannot connect to inverter at {self.host}:{self.port}: {e}")
            raise

    def start(self):
        self._db_stop_event = threading.Event()
        if self.db_path:
            self._db_writer_thread = threading.Thread(
                target=_db_writer, args=(self.db_path, _db_write_interval), daemon=True
            )
            self._db_writer_thread.start()
            print(f"SQLite logging enabled: {self.db_path}")

        self._poller = threading.Thread(
            target=self._poller_loop, args=(self.interval,), daemon=True
        )
        self._poller.start()

    def _poller_loop(self, interval):
        while True:
            try:
                if self.solarman is None:
                    try:
                        self.solarman = PySolarmanV5(
                            self.host,
                            self.sn,
                            port=self.port,
                            mb_slave_id=MB_SLAVE_ID,
                            timeout=5,
                            retry_count=3,
                        )
                        self.solarman.read_holding_registers(79, 1)
                        print("Reconnected to inverter.")
                    except Exception as e:
                        print(f"Reconnect failed: {e}")
                        self.solarman = None
                        time.sleep(5)
                        continue
                vals = read_all(self.solarman)
                if vals:
                    with self.data_lock:
                        self.latest_data = vals
                    with _buffer_lock:
                        _reading_buffer.append(vals)
            except Exception as e:
                print(f"Poller error: {e}")
                self.solarman = None
            time.sleep(interval)

    def get_data(self):
        with self.data_lock:
            return self.latest_data

    def get_db_conn(self):
        return _db_conn

    def stop(self):
        if self.solarman:
            self.solarman.disconnect()
        _db_stop_event.set()
        _flush_last_batch()
        if _db_conn:
            _db_conn.close()
