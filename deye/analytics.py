import os
import sqlite3
import time
from datetime import datetime, timezone


def init_analytics(db_path):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""CREATE TABLE IF NOT EXISTS minute_agg (
        timestamp INTEGER PRIMARY KEY,
        pv_wh REAL,
        grid_import_wh REAL,
        grid_export_wh REAL,
        battery_charge_wh REAL,
        battery_discharge_wh REAL
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS day_agg (
        day TEXT PRIMARY KEY,
        pv_kwh REAL,
        grid_import_kwh REAL,
        grid_export_kwh REAL,
        battery_charge_kwh REAL,
        battery_discharge_kwh REAL
    )""")
    conn.commit()
    return conn


def update_analytics(analytics_conn, ts, readings):
    pv_wh = 0.0
    grid_import_wh = 0.0
    grid_export_wh = 0.0
    battery_charge_wh = 0.0
    battery_discharge_wh = 0.0

    pv_power = readings.get('PV1 Power') or 0
    pv_power += readings.get('PV2 Power') or 0
    if pv_power > 0:
        pv_wh = pv_power / 60.0

    grid_power = readings.get('Grid Power') or 0
    if grid_power > 0:
        grid_import_wh = grid_power / 60.0
    elif grid_power < 0:
        grid_export_wh = abs(grid_power) / 60.0

    battery_power = readings.get('Battery Power') or 0
    if battery_power < 0:
        battery_charge_wh = abs(battery_power) / 60.0
    elif battery_power > 0:
        battery_discharge_wh = battery_power / 60.0

    conn = analytics_conn
    conn.execute("""INSERT OR REPLACE INTO minute_agg
        (timestamp, pv_wh, grid_import_wh, grid_export_wh, battery_charge_wh, battery_discharge_wh)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (ts, pv_wh, grid_import_wh, grid_export_wh, battery_charge_wh, battery_discharge_wh))

    day = datetime.fromtimestamp(ts, tz=timezone.utc).strftime('%Y-%m-%d')
    conn.execute("""INSERT INTO day_agg
        (day, pv_kwh, grid_import_kwh, grid_export_kwh, battery_charge_kwh, battery_discharge_kwh)
        VALUES (?, 0, 0, 0, 0, 0)
        ON CONFLICT(day) DO NOTHING""", (day,))

    conn.execute("""UPDATE day_agg SET
        pv_kwh = pv_kwh + ?,
        grid_import_kwh = grid_import_kwh + ?,
        grid_export_kwh = grid_export_kwh + ?,
        battery_charge_kwh = battery_charge_kwh + ?,
        battery_discharge_kwh = battery_discharge_kwh + ?
        WHERE day = ?""",
        (pv_wh / 1000.0, grid_import_wh / 1000.0, grid_export_wh / 1000.0,
         battery_charge_wh / 1000.0, battery_discharge_wh / 1000.0, day))

    conn.commit()


def get_period_totals(analytics_conn, start_ts, end_ts):
    cur = analytics_conn.execute("""
        SELECT
            COALESCE(SUM(pv_wh), 0) as pv_wh,
            COALESCE(SUM(grid_import_wh), 0) as grid_import_wh,
            COALESCE(SUM(grid_export_wh), 0) as grid_export_wh,
            COALESCE(SUM(battery_charge_wh), 0) as battery_charge_wh,
            COALESCE(SUM(battery_discharge_wh), 0) as battery_discharge_wh
        FROM minute_agg
        WHERE timestamp >= ? AND timestamp <= ?
    """, (start_ts, end_ts))
    row = cur.fetchone()
    pv = row[0]
    gi = row[1]
    ge = row[2]
    bc = row[3]
    bd = row[4]
    consumption = pv + gi - ge - bc + bd
    return {
        'pv_kwh': round(pv / 1000.0, 4),
        'grid_import_kwh': round(gi / 1000.0, 4),
        'consumption_kwh': round(consumption / 1000.0, 4),
    }


def get_daily_data(analytics_conn, start_ts, end_ts):
    cur = analytics_conn.execute("""
        SELECT day, pv_kwh, grid_import_kwh, grid_export_kwh,
               battery_charge_kwh, battery_discharge_kwh
        FROM day_agg
        WHERE day >= ? AND day <= ?
        ORDER BY day
    """, (
        datetime.fromtimestamp(start_ts, tz=timezone.utc).strftime('%Y-%m-%d'),
        datetime.fromtimestamp(end_ts, tz=timezone.utc).strftime('%Y-%m-%d'),
    ))
    return [{'day': r[0], 'pv_kwh': r[1], 'grid_import_kwh': r[2],
             'grid_export_kwh': r[3], 'battery_charge_kwh': r[4],
             'battery_discharge_kwh': r[5],
             'consumption_kwh': r[1] + r[2] - r[3] - r[4] + r[5]} for r in cur.fetchall()]


def get_period_data(analytics_conn, start_ts, end_ts, range_type='month'):
    if range_type in ('week', 'month'):
        cur = analytics_conn.execute("""
            SELECT
                strftime('%Y-%m-%d', timestamp, 'unixepoch', 'utc') as period,
                SUM(pv_wh) as pv_wh,
                SUM(grid_import_wh) as grid_import_wh,
                SUM(grid_export_wh) as grid_export_wh,
                SUM(battery_charge_wh) as battery_charge_wh,
                SUM(battery_discharge_wh) as battery_discharge_wh
            FROM minute_agg
            WHERE timestamp >= ? AND timestamp <= ?
            GROUP BY strftime('%Y-%m-%d', timestamp, 'unixepoch', 'utc')
            ORDER BY period
        """, (start_ts, end_ts))
        return [{'period': r[0], 'pv_kwh': r[1] / 1000.0, 'grid_import_kwh': r[2] / 1000.0,
                 'grid_export_kwh': r[3] / 1000.0, 'battery_charge_kwh': r[4] / 1000.0,
                 'battery_discharge_kwh': r[5] / 1000.0,
                 'consumption_kwh': (r[1] + r[2] - r[3] - r[4] + r[5]) / 1000.0} for r in cur.fetchall()]
    elif range_type == 'year':
        cur = analytics_conn.execute("""
            SELECT
                strftime('%Y-%m', timestamp, 'unixepoch', 'utc') as period,
                SUM(pv_wh) as pv_wh,
                SUM(grid_import_wh) as grid_import_wh,
                SUM(grid_export_wh) as grid_export_wh,
                SUM(battery_charge_wh) as battery_charge_wh,
                SUM(battery_discharge_wh) as battery_discharge_wh
            FROM minute_agg
            WHERE timestamp >= ? AND timestamp <= ?
            GROUP BY strftime('%Y-%m', timestamp, 'unixepoch', 'utc')
            ORDER BY period
        """, (start_ts, end_ts))
        return [{'period': r[0], 'pv_kwh': r[1] / 1000.0, 'grid_import_kwh': r[2] / 1000.0,
                 'grid_export_kwh': r[3] / 1000.0, 'battery_charge_kwh': r[4] / 1000.0,
                 'battery_discharge_kwh': r[5] / 1000.0,
                 'consumption_kwh': (r[1] + r[2] - r[3] - r[4] + r[5]) / 1000.0} for r in cur.fetchall()]
    else:
        granularity_seconds = _get_granularity(start_ts, end_ts)
        cur = analytics_conn.execute("""
            SELECT
                strftime('%Y-%m-%d %H:%M', timestamp, 'unixepoch', 'utc') as period,
                SUM(pv_wh) as pv_wh,
                SUM(grid_import_wh) as grid_import_wh,
                SUM(grid_export_wh) as grid_export_wh,
                SUM(battery_charge_wh) as battery_charge_wh,
                SUM(battery_discharge_wh) as battery_discharge_wh
            FROM minute_agg
            WHERE timestamp >= ? AND timestamp <= ?
            GROUP BY strftime('%Y-%m-%d %H:%M', timestamp / ? * ?, 'unixepoch', 'utc')
            ORDER BY period
        """, (start_ts, end_ts, granularity_seconds, granularity_seconds))
        return [{'period': r[0], 'pv_kwh': r[1] / 1000.0, 'grid_import_kwh': r[2] / 1000.0,
                 'grid_export_kwh': r[3] / 1000.0, 'battery_charge_kwh': r[4] / 1000.0,
                 'battery_discharge_kwh': r[5] / 1000.0,
                 'consumption_kwh': (r[1] + r[2] - r[3] - r[4] + r[5]) / 1000.0} for r in cur.fetchall()]


def _get_granularity(start_ts, end_ts):
    span = end_ts - start_ts
    if span <= 2 * 86400:
        return 3600
    elif span <= 180 * 86400:
        return 7 * 86400
    else:
        return 30 * 86400
