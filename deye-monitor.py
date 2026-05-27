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
import csv
import datetime
import json
import signal
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

from pysolarmanv5 import PySolarmanV5
from pysolarmanv5.pysolarmanv5 import NoSocketAvailableError
from pymodbus.exceptions import ModbusException

# ─── Configuration ──────────────────────────────────────────────────────────

INVERTER_IP = "192.168.1.2"
INVERTER_PORT = 8899
INVERTER_SN = 3168400438
MB_SLAVE_ID = 1
LOG_FILE = "deye-data.csv"
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
        (182, "Battery Temp", "°C", 0.1, 0, 1000),
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

CSV_HEADER = ["Timestamp"] + [r[1] for r in ALL_REGISTERS]

# ─── Helpers ────────────────────────────────────────────────────────────────

def read_chunk(solarman, start_addr, count):
    try:
        raw = solarman.read_holding_registers(start_addr, count)
        return list(raw)
    except ModbusException:
        return None
    except Exception as e:
        print(f"  Read error at addr {start_addr}: {e}")
        return None


def read_all(solarman):
    if not ALL_REGISTERS:
        return {}

    MAX_CHUNK = 120
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

        for addr, name, unit, scale, sign_bit, *rest in chunk:
            temp_offset = rest[0] if rest else 0
            idx = addr - start
            if idx < len(raw):
                val = raw[idx]
                if sign_bit and val >= (1 << sign_bit):
                    val = val - (1 << 16)
                if temp_offset:
                    val = (val - temp_offset) * scale
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
        for reg in regs:
            addr, name, unit, scale, sign_bit = reg[:5]
            val = values.get(name)
            if val is None:
                print(f"{name}  ---")
            elif unit == "W":
                print(f"{name}  {format_power(val)}")
            else:
                print(f"{name}  {val:.2f} {unit}")
    print()


def write_csv_row(filepath, values):
    exists = os.path.isfile(filepath)
    with open(filepath, "a", newline="") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(CSV_HEADER)
        row = [datetime.datetime.now().isoformat()]
        for reg in ALL_REGISTERS:
            name = reg[1]
            row.append(values.get(name))
        writer.writerow(row)


def signal_handler(signum, frame):
    print("\n\nStopped.")
    sys.exit(0)


# ─── HTML Dashboard ─────────────────────────────────────────────────────────

DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PV Monitor</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    background: #0d1117;
    color: #c9d1d9;
    min-height: 100vh;
    padding: 16px;
}

h1 {
    text-align: center;
    font-size: 1.4rem;
    font-weight: 600;
    color: #58a6ff;
    margin-bottom: 16px;
    letter-spacing: 0.5px;
}

.quad {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 12px;
    height: calc(100vh - 80px);
    max-height: 700px;
}

.card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.card-title {
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid #21262d;
}

.card-title .icon { margin-right: 6px; }

.solar .card-title { color: #f0883e; }
.grid .card-title { color: #3fb950; }
.load .card-title { color: #d29922; }
.battery .card-title { color: #a371f7; }

.readings {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 6px;
}

.row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding: 4px 0;
}

.row-label {
    font-size: 0.8rem;
    color: #8b949e;
    flex-shrink: 0;
    margin-right: 12px;
}

.row-value {
    font-size: 1.1rem;
    font-weight: 600;
    font-variant-numeric: tabular-nums;
    text-align: right;
}

.row-value.w { color: #f0883e; }
.row-value.v { color: #79c0ff; }
.row-value.a { color: #ffa657; }
.row-value.watts { color: #d2a8ff; }
.row-value.freq { color: #7ee787; }
.row-value.pct { color: #a371f7; }
.row-value.temp { color: #79c0ff; }
.row-value.na { color: #484f58; }

.status-bar {
    text-align: center;
    font-size: 0.7rem;
    color: #484f58;
    margin-top: 8px;
}

.status-bar .error { color: #f85149; }

/* Large values */
.big {
    font-size: 2rem;
    font-weight: 700;
    text-align: center;
    margin: 4px 0;
}

/* Responsive */
@media (max-width: 600px) {
    body { padding: 8px; }
    .quad { gap: 8px; height: calc(100vh - 60px); }
    .card { padding: 12px; border-radius: 8px; }
    .card-title { font-size: 0.75rem; }
    .row-label { font-size: 0.7rem; margin-right: 8px; }
    .row-value { font-size: 0.95rem; }
    .big { font-size: 1.5rem; }
    h1 { font-size: 1.1rem; }
}

@media (max-height: 500px) and (orientation: landscape) {
    body { padding: 4px; }
    .quad { gap: 6px; height: calc(100vh - 40px); }
    .card { padding: 8px; }
    .card-title { font-size: 0.7rem; margin-bottom: 6px; }
    .row-label { font-size: 0.65rem; }
    .row-value { font-size: 0.85rem; }
    .big { font-size: 1.3rem; }
}
</style>
</head>
<body>
<h1>Photovoltaic Monitor</h1>
<div class="quad">
    <div class="card solar">
        <div class="card-title"><span class="icon">&#9729;</span>Solar PV</div>
        <div class="readings" id="solar"></div>
    </div>
    <div class="card grid">
        <div class="card-title"><span class="icon">&#9889;</span>Grid</div>
        <div class="readings" id="grid"></div>
    </div>
    <div class="card load">
        <div class="card-title"><span class="icon">&#128268;</span>Load</div>
        <div class="readings" id="load"></div>
    </div>
    <div class="card battery">
        <div class="card-title"><span class="icon">&#128267;</span>Battery</div>
        <div class="readings" id="battery"></div>
    </div>
</div>
<div class="status-bar" id="status">Connecting...</div>

<script>
const layouts = {
    solar: [
        { label: 'PV1 Power', key: 'PV1 Power', cls: 'w' },
        { label: 'PV2 Power', key: 'PV2 Power', cls: 'w' },
        { label: 'Total Power', key: '_total_pv', cls: 'w' },
        { label: 'PV1 Voltage', key: 'PV1 Voltage', cls: 'v' },
        { label: 'PV1 Current', key: 'PV1 Current', cls: 'a' },
        { label: 'PV2 Voltage', key: 'PV2 Voltage', cls: 'v' },
        { label: 'PV2 Current', key: 'PV2 Current', cls: 'a' },
    ],
    grid: [
        { label: 'Grid Power', key: 'Grid Power', cls: 'watts' },
        { label: 'CT Power', key: 'Grid CT Power', cls: 'watts' },
        { label: 'Grid Voltage', key: 'Grid Voltage', cls: 'v' },
        { label: 'Grid Current L', key: 'Grid Current L', cls: 'a' },
        { label: 'Grid Freq', key: 'Grid Frequency', cls: 'freq' },
    ],
    load: [
        { label: 'Load Total', key: 'Load Power Total', cls: 'watts' },
        { label: 'Load L1', key: 'Load Power L1', cls: 'watts' },
        { label: 'Load Voltage L1', key: 'Load Voltage L1', cls: 'v' },
        { label: 'Load Current L1', key: 'Load Current L1', cls: 'a' },
        { label: 'Load Freq', key: 'Load Frequency', cls: 'freq' },
    ],
    battery: [
        { label: 'Battery Power', key: 'Battery Power', cls: 'watts' },
        { label: 'SOC', key: 'Battery SOC', cls: 'pct' },
        { label: 'Battery Voltage', key: 'Battery Voltage', cls: 'v' },
        { label: 'Battery Current', key: 'Battery Current', cls: 'a' },
        { label: 'Battery Temp', key: 'Battery Temp', cls: 'temp' },
        { label: 'Charge Limit', key: 'Batt Charge Limit', cls: 'a' },
        { label: 'Discharge Limit', key: 'Batt Discharge Limit', cls: 'a' },
    ],
};

function fmt(val, unit) {
    if (val === null || val === undefined || val === 'N/A') return '<span class="row-value na">N/A</span>';
    if (unit === 'W') {
        const w = parseFloat(val);
        if (isNaN(w)) return '<span class="row-value na">N/A</span>';
        if (Math.abs(w) >= 1000) return '<span class="row-value ' + (layouts._tempCls || 'watts') + '">' + (w/1000).toFixed(2) + ' kW</span>';
        return '<span class="row-value ' + (layouts._tempCls || 'watts') + '">' + w.toFixed(0) + ' W</span>';
    }
    return '<span class="row-value ' + (layouts._tempCls || '') + '">' + parseFloat(val).toFixed(2) + ' ' + unit + '</span>';
}

function render(data) {
    for (const [zone, fields] of Object.entries(layouts)) {
        const el = document.getElementById(zone);
        let html = '';
        for (const f of fields) {
            let val = data[f.key];
            let unit = '';
            if (f.key === '_total_pv') {
                const p1 = parseFloat(data['PV1 Power'] || 0);
                const p2 = parseFloat(data['PV2 Power'] || 0);
                const total = p1 + p2;
                if (Math.abs(total) >= 1000) {
                    val = (total/1000).toFixed(2) + ' kW';
                } else {
                    val = total.toFixed(0) + ' W';
                }
                html += '<div class="row"><span class="row-label">' + f.label + '</span>' +
                    '<span class="row-value w" style="font-size:1.3rem">' + val + '</span></div>';
                continue;
            }
            if (f.key === 'Battery SOC') unit = '%';
            else if (f.key === 'Battery Temp') unit = '°C';
            else if (f.key === 'Grid Frequency' || f.key === 'Load Frequency') unit = 'Hz';
            else if (f.key === 'Inverter Freq') unit = 'Hz';
            else if (f.key === 'AUX Frequency') unit = 'Hz';
            else if (f.key === 'Grid Voltage' || f.key === 'PV1 Voltage' || f.key === 'PV2 Voltage' || f.key === 'Battery Voltage' || f.key === 'AUX Voltage' || f.key === 'Load Voltage L1') unit = 'V';
            else if (f.key === 'PV1 Current' || f.key === 'PV2 Current' || f.key === 'Grid Current L' || f.key === 'Grid Current N' || f.key === 'Battery Current' || f.key === 'Batt Charge Limit' || f.key === 'Batt Discharge Limit' || f.key === 'Load Current L1') unit = 'A';
            else if (f.key === 'PV1 Power' || f.key === 'PV2 Power' || f.key === 'Grid Power' || f.key === 'Grid CT Power' || f.key === 'Load Power Total' || f.key === 'Load Power L1' || f.key === 'Load Power L2' || f.key === 'Battery Power') unit = 'W';
            else unit = '';
            html += '<div class="row"><span class="row-label">' + f.label + '</span>' + fmt(val, unit) + '</div>';
        }
        el.innerHTML = html;
    }
}

function update() {
    fetch('/PV')
        .then(r => r.json())
        .then(data => {
            render(data);
            document.getElementById('status').textContent = 'Updated ' + new Date().toLocaleTimeString();
            document.getElementById('status').className = 'status-bar';
        })
        .catch(e => {
            document.getElementById('status').innerHTML = '<span class="error">Error: ' + e.message + '</span>';
        });
}

update();
setInterval(update, 3000);
</script>
</body>
</html>
"""


# ─── HTTP Handler ───────────────────────────────────────────────────────────

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
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(DASHBOARD_HTML.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass


def data_poller():
    global solarman, latest_data
    while True:
        try:
            vals = read_all(solarman)
            if vals:
                with data_lock:
                    latest_data = vals
        except Exception as e:
            print(f"Poller error: {e}")
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
    parser.add_argument("--log-file", default=LOG_FILE,
                        help=f"CSV log file (default: {LOG_FILE})")
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
    poller = threading.Thread(target=data_poller, daemon=True)
    poller.start()

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
