#!/home/me/tools/deye/deye-env/bin/python3
# -*- coding: utf-8 -*-
"""Deye SUN-6k-SG03LP1-EU Solarman V5 / Modbus TCP reader.

Reads power statistics from a Deye hybrid inverter via Solarman V5 protocol
(port 8899). Runs self-contained — finds its own Python environment.

Usage:
    ./deye-monitor.py              # One-shot read
    ./deye-monitor.py --interval 60  # Continuous, log every 60s
    ./deye-monitor.py --host 192.168.1.102 --interval 60  # Both
"""

import argparse
import csv
import datetime
import os
import signal
import sys
import time

try:
    from pysolarmanv5 import PySolarmanV5
    from pymodbus.exceptions import ModbusException
except ImportError:
    print("Error: pysolarmanv5 not installed.")
    print("Run: pip install pysolarmanv5")
    sys.exit(1)

# ─── Configuration ──────────────────────────────────────────────────────────

INVERTER_IP = "192.168.1.102"
INVERTER_PORT = 8899
INVERTER_SN = 3168400438
MB_SLAVE_ID = 1
LOG_FILE = "deye-data.csv"

# ─── Modbus Register Definitions ────────────────────────────────────────────
# Based on sunsynk project register map for single-phase Deye inverters.
# Source: https://github.com/kellerza/sunsynk

REGISTER_GROUPS = {
    "Solar PV 1": [
        (109, "PV1 Voltage", "V", 0.1, 0),
        (110, "PV1 Current", "A", 0.1, 0),
        (186, "PV1 Power", "W", -1, 0),
    ],
    "Solar PV 2": [
        (111, "PV2 Voltage", "V", 0.1, 0),
        (112, "PV2 Current", "A", 0.1, 0),
        (187, "PV2 Power", "W", -1, 0),
    ],
    "Inverter": [
        (154, "Inverter Voltage", "V", 0.1, 0),
        (164, "Inverter Current", "A", 0.01, 0),
        (175, "Inverter Power", "W", -1, 0),
        (193, "Inverter Freq", "Hz", 0.01, 0),
    ],
    "Grid": [
        (79, "Grid Frequency", "Hz", 0.01, 0),
        (150, "Grid Voltage", "V", 0.1, 0),
        (160, "Grid Current L", "A", 0.01, 0),
        (161, "Grid Current N", "A", 0.01, 0),
        (169, "Grid Power", "W", -1, 0),
        (172, "Grid CT Power", "W", -1, 0),
    ],
    "Load": [
        (176, "Load Power L1", "W", -1, 0),
        (177, "Load Power L2", "W", -1, 0),
        (178, "Load Power Total", "W", -1, 0),
        (192, "Load Frequency", "Hz", 0.01, 0),
    ],
    "Battery": [
        (182, "Battery Temp", "°C", 0.1, 0),
        (183, "Battery Voltage", "V", 0.01, 0),
        (184, "Battery SOC", "%", 1, 0),
        (190, "Battery Power", "W", -1, 0),
        (191, "Battery Current", "A", -0.01, 0),
        (314, "Batt Charge Limit", "A", -1, 0),
        (315, "Batt Discharge Limit", "A", -1, 0),
    ],
    "AUX / Generator": [
        (166, "AUX Power", "W", -1, 0),
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
    """Read a chunk of holding registers via Solarman V5."""
    try:
        raw = solarman.read_holding_registers(start_addr, count)
        return list(raw)
    except ModbusException:
        return None
    except Exception as e:
        print(f"  Read error at addr {start_addr}: {e}")
        return None


def read_all(solarman):
    """Read all registers in chunks (max 120 per Solarman request).
    Returns dict of {name: value} or None."""
    if not ALL_REGISTERS:
        return {}

    MAX_CHUNK = 120  # Solarman v5 max per request
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
                values[name] = round(val * scale, 2)
            else:
                values[name] = None
        i = chunk_end

    return values if all_ok else None


def format_power(watts):
    """Format watts to kW if > 1000W."""
    if watts is None:
        return "N/A"
    if abs(watts) >= 1000:
        return f"{watts/1000:+.2f} kW"
    return f"{watts:+.0f} W"


def print_header():
    print("\n" + "=" * 70)
    print("  Deye SUN-6k-SG03LP1-EU  |  Solarman V5 Monitor")
    print("  Port: 8899  |  Slave: 1")
    print("=" * 70)


def print_readings(values, timestamp=None):
    ts = timestamp or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n  {ts}")
    print("-" * 70)

    for group_name, regs in REGISTER_GROUPS.items():
        print(f"\n  [{group_name}]")
        for addr, name, unit, scale, sign_bit in regs:
            val = values.get(name)
            if val is None:
                print(f"    {name:<25s}  {'---':>10s}")
            elif unit == "W":
                print(f"    {name:<25s}  {format_power(val):>10s}")
            else:
                print(f"    {name:<25s}  {val:>10.2f} {unit}")

    grid_power = values.get("Grid Power")
    pv_power = (values.get("PV1 Power") or 0) + (values.get("PV2 Power") or 0)
    load_power = values.get("Load Power Total")
    batt_power = values.get("Battery Power")

    print("\n" + "-" * 70)
    print("  SUMMARY")
    print("-" * 70)
    print(f"    PV Generation:           {format_power(pv_power)}")
    print(f"    Grid Import/Export:      {format_power(grid_power)}")
    print(f"    Load Consumption:        {format_power(load_power)}")
    print(f"    Battery Charge/Disch:    {format_power(batt_power)}")
    print()


def write_csv_row(filepath, values):
    exists = os.path.isfile(filepath)
    with open(filepath, "a", newline="") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(CSV_HEADER)
        row = [datetime.datetime.now().isoformat()]
        for _, name, _, _, _ in ALL_REGISTERS:
            row.append(values.get(name))
        writer.writerow(row)


def signal_handler(signum, frame):
    print("\n\nStopped.")
    sys.exit(0)


# ─── Main ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Read power stats from Deye SUN-6k-SG03LP1-EU inverter"
    )
    parser.add_argument(
        "--host", default=INVERTER_IP,
        help=f"Inverter IP address (default: {INVERTER_IP})"
    )
    parser.add_argument(
        "--port", type=int, default=INVERTER_PORT,
        help=f"Modbus port (default: {INVERTER_PORT})"
    )
    parser.add_argument(
        "--interval", type=int, default=0,
        help="Logging interval in seconds (0 = one-shot, default: 0)"
    )
    parser.add_argument(
        "--log-file", default=LOG_FILE,
        help=f"CSV log file path (default: {LOG_FILE})"
    )
    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal_handler)

    print_header()
    print(f"\n  Connecting to {args.host}:{args.port} ...")
    print(f"  Serial number: {INVERTER_SN}")

    solarman = PySolarmanV5(
        args.host,
        INVERTER_SN,
        port=args.port,
        mb_slave_id=MB_SLAVE_ID,
        timeout=5,
        retry_count=3,
    )

    try:
        # Test connection by reading a known register
        test = solarman.read_holding_registers(79, 1)  # Grid frequency
        print(f"  Connected! Grid freq register: {test}\n")
    except Exception as e:
        print(f"\n  ERROR: Cannot connect to inverter.")
        print(f"  Details: {e}")
        print("\n  Common issues:")
        print("    - Wrong serial number (check sticker on inverter/logger)")
        print("    - Inverter not on the same network")
        print("    - Solarman protocol not enabled in inverter settings")
        sys.exit(1)

    if args.interval > 0:
        print(f"  Logging every {args.interval}s to {args.log_file}")
        print(f"  Press Ctrl+C to stop.\n")
        try:
            while True:
                values = read_all(solarman)
                if values:
                    print_readings(values)
                    write_csv_row(args.log_file, values)
                else:
                    print("  Warning: Read failed, retrying...")
                time.sleep(args.interval)
        except KeyboardInterrupt:
            signal_handler(None, None)
    else:
        values = read_all(solarman)
        if values:
            print_readings(values)
        else:
            print("\n  ERROR: Failed to read registers.")
            print("  Possible causes:")
            print("    - Serial number is incorrect")
            print("    - Inverter firmware blocks Modbus access")
            print("    - Data logger (LSW3/LSW4) not properly configured")

    solarman.disconnect()


if __name__ == "__main__":
    main()
