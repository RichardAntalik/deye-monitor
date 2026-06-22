#!/usr/bin/env python3
"""Rebuild analytics database from readings data."""
import sqlite3
import sys
from datetime import datetime, timezone


def rebuild(source_db, dest_db):
    src = sqlite3.connect(source_db)
    dst = sqlite3.connect(dest_db)

    dst.execute("PRAGMA journal_mode=WAL")
    dst.execute("""CREATE TABLE IF NOT EXISTS day_agg (
        day TEXT PRIMARY KEY,
        pv_kwh REAL,
        grid_import_kwh REAL,
        grid_export_kwh REAL,
        battery_charge_kwh REAL,
        battery_discharge_kwh REAL
    )""")

    cur = src.cursor()
    cur.execute("SELECT timestamp, `PV1 Power`, `PV2 Power`, `Grid Power`, `Battery Power` FROM readings ORDER BY timestamp")
    rows = cur.fetchall()
    total = len(rows)
    print(f"Processing {total} readings...")

    for i, row in enumerate(rows):
        ts, pv1, pv2, grid_pwr, batt_pwr = row
        pv_wh = 0.0
        grid_import_wh = 0.0
        grid_export_wh = 0.0
        battery_charge_wh = 0.0
        battery_discharge_wh = 0.0

        pv_power = (pv1 or 0) + (pv2 or 0)
        if pv_power > 0:
            pv_wh = pv_power / 60.0

        if grid_pwr > 0:
            grid_import_wh = grid_pwr / 60.0
        elif grid_pwr < 0:
            grid_export_wh = abs(grid_pwr) / 60.0

        if batt_pwr < 0:
            battery_charge_wh = abs(batt_pwr) / 60.0
        elif batt_pwr > 0:
            battery_discharge_wh = batt_pwr / 60.0

        day = datetime.fromtimestamp(ts, tz=timezone.utc).strftime('%Y-%m-%d')
        dst.execute("""INSERT INTO day_agg
            (day, pv_kwh, grid_import_kwh, grid_export_kwh, battery_charge_kwh, battery_discharge_kwh)
            VALUES (?, 0, 0, 0, 0, 0)
            ON CONFLICT(day) DO NOTHING""", (day,))

        dst.execute("""UPDATE day_agg SET
            pv_kwh = pv_kwh + ?,
            grid_import_kwh = grid_import_kwh + ?,
            grid_export_kwh = grid_export_kwh + ?,
            battery_charge_kwh = battery_charge_kwh + ?,
            battery_discharge_kwh = battery_discharge_kwh + ?
            WHERE day = ?""",
            (pv_wh / 1000.0, grid_import_wh / 1000.0, grid_export_wh / 1000.0,
             battery_charge_wh / 1000.0, battery_discharge_wh / 1000.0, day))

        if (i + 1) % 5000 == 0:
            dst.commit()
            print(f"  {i+1}/{total} ({100*(i+1)//total}%)")

    dst.commit()

    c = dst.cursor()
    c.execute("SELECT COUNT(*) FROM day_agg")
    print(f"day_agg: {c.fetchone()[0]} rows")
    c.execute("SELECT MIN(day), MAX(day) FROM day_agg")
    r = c.fetchone()
    print(f"Date range: {r[0]} to {r[1]}")

    src.close()
    dst.close()
    print("Done.")


if __name__ == '__main__':
    source = sys.argv[1] if len(sys.argv) > 1 else '/mnt/storage/deye_db/test.db'
    dest = sys.argv[2] if len(sys.argv) > 2 else '/mnt/storage/deye_db/analytics.db'
    rebuild(source, dest)
