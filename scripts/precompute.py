#!/usr/bin/env python3
"""Pre-compute analytics data from historical readings.

Usage:
    python scripts/precompute.py [--db deye/test.db] [--analytics deye/analytics.db]
"""
import argparse
import os
import sqlite3
from datetime import datetime, timezone


def precompute(readings_db, analytics_db, month=None):
    readings_conn = sqlite3.connect(readings_db)
    cur = readings_conn.cursor()
    cur.execute("SELECT MIN(timestamp), MAX(timestamp), COUNT(*) FROM readings")
    min_ts, max_ts, total = cur.fetchone()
    print(f"Data range: {datetime.fromtimestamp(min_ts).strftime('%Y-%m-%d %H:%M')} to {datetime.fromtimestamp(max_ts).strftime('%Y-%m-%d %H:%M')}")
    print(f"Total readings: {total}")

    analytics_conn = sqlite3.connect(analytics_db)
    analytics_conn.execute("PRAGMA journal_mode=WAL")
    analytics_conn.execute("""CREATE TABLE IF NOT EXISTS day_agg (
        day TEXT PRIMARY KEY,
        pv_kwh REAL,
        grid_import_kwh REAL,
        grid_export_kwh REAL,
        battery_charge_kwh REAL,
        battery_discharge_kwh REAL
    )""")
    analytics_conn.commit()

    filter_month = month
    if filter_month:
        print(f"Filtering to month: {filter_month}")
        cur.execute("""SELECT timestamp, `PV1 Power`, `PV2 Power`, `Grid Power`, `Battery Power`
            FROM readings
            WHERE strftime('%Y-%m', timestamp, 'unixepoch', 'utc') = ?
            ORDER BY timestamp""", (filter_month,))
    else:
        cur.execute("SELECT timestamp, `PV1 Power`, `PV2 Power`, `Grid Power`, `Battery Power` FROM readings ORDER BY timestamp")
    rows = cur.fetchall()
    total = len(rows)
    if filter_month:
        print(f"Filtered readings for {filter_month}: {total}")
    count = 0
    for row in rows:
        ts, pv1, pv2, grid, battery = row
        pv_power = (pv1 or 0) + (pv2 or 0)
        pv_wh = pv_power / 60.0 if pv_power > 0 else 0.0

        if grid > 0:
            grid_import_wh = grid / 60.0
            grid_export_wh = 0.0
        elif grid < 0:
            grid_import_wh = 0.0
            grid_export_wh = abs(grid) / 60.0
        else:
            grid_import_wh = 0.0
            grid_export_wh = 0.0

        if battery < 0:
            battery_charge_wh = abs(battery) / 60.0
            battery_discharge_wh = 0.0
        elif battery > 0:
            battery_charge_wh = 0.0
            battery_discharge_wh = battery / 60.0
        else:
            battery_charge_wh = 0.0
            battery_discharge_wh = 0.0

        day = datetime.fromtimestamp(ts, tz=timezone.utc).strftime('%Y-%m-%d')
        analytics_conn.execute("""INSERT INTO day_agg
            (day, pv_kwh, grid_import_kwh, grid_export_kwh, battery_charge_kwh, battery_discharge_kwh)
            VALUES (?, 0, 0, 0, 0, 0)
            ON CONFLICT(day) DO NOTHING""", (day,))
        analytics_conn.execute("""UPDATE day_agg SET
            pv_kwh = pv_kwh + ?,
            grid_import_kwh = grid_import_kwh + ?,
            grid_export_kwh = grid_export_kwh + ?,
            battery_charge_kwh = battery_charge_kwh + ?,
            battery_discharge_kwh = battery_discharge_kwh + ?
            WHERE day = ?""",
            (pv_wh / 1000.0, grid_import_wh / 1000.0, grid_export_wh / 1000.0,
             battery_charge_wh / 1000.0, battery_discharge_wh / 1000.0, day))

        count += 1
        if count % 1000 == 0:
            print(f"Processed {count}/{total} rows")

    analytics_conn.commit()
    print(f"Done. Processed {count}/{total} rows")
    readings_conn.close()
    analytics_conn.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pre-compute analytics from historical readings')
    parser.add_argument('--db', default='deye/test.db', help='Path to readings database')
    parser.add_argument('--analytics', default='deye/analytics.db', help='Path to analytics database')
    parser.add_argument('--month', default=None, help='Filter to YYYY-MM (e.g. 2026-06)')
    args = parser.parse_args()
    precompute(args.db, args.analytics, args.month)
