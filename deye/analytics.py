import sqlite3
from datetime import datetime, timezone


def init_analytics(db_path):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
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
    start_day = datetime.fromtimestamp(start_ts, tz=timezone.utc).strftime('%Y-%m-%d')
    end_day = datetime.fromtimestamp(end_ts, tz=timezone.utc).strftime('%Y-%m-%d')

    cur = analytics_conn.execute("""
        SELECT
            COALESCE(SUM(pv_kwh), 0) as pv_kwh,
            COALESCE(SUM(grid_import_kwh), 0) as grid_import_kwh,
            COALESCE(SUM(grid_export_kwh), 0) as grid_export_kwh,
            COALESCE(SUM(battery_charge_kwh), 0) as battery_charge_kwh,
            COALESCE(SUM(battery_discharge_kwh), 0) as battery_discharge_kwh
        FROM day_agg
        WHERE day >= ? AND day <= ?
    """, (start_day, end_day))
    row = cur.fetchone()
    pv = row[0]
    gi = row[1]
    ge = row[2]
    bc = row[3]
    bd = row[4]

    consumption = pv + gi - ge - bc + bd
    return {
        'pv_kwh': round(pv, 4),
        'grid_import_kwh': round(gi, 4),
        'consumption_kwh': round(consumption, 4),
    }


def get_period_data(analytics_conn, start_ts, end_ts, range_type='month'):
    start_day = datetime.fromtimestamp(start_ts, tz=timezone.utc).strftime('%Y-%m-%d')
    end_day = datetime.fromtimestamp(end_ts, tz=timezone.utc).strftime('%Y-%m-%d')

    if range_type == 'year':
        cur = analytics_conn.execute("""
            SELECT strftime('%Y-%m', day) as period,
                   SUM(pv_kwh) as pv_kwh,
                   SUM(grid_import_kwh) as grid_import_kwh,
                   SUM(grid_export_kwh) as grid_export_kwh,
                   SUM(battery_charge_kwh) as battery_charge_kwh,
                   SUM(battery_discharge_kwh) as battery_discharge_kwh
            FROM day_agg
            WHERE day >= ? AND day <= ?
            GROUP BY period
            ORDER BY period
        """, (start_day, end_day))
    else:
        cur = analytics_conn.execute("""
            SELECT day as period,
                   pv_kwh, grid_import_kwh, grid_export_kwh,
                   battery_charge_kwh, battery_discharge_kwh
            FROM day_agg
            WHERE day >= ? AND day <= ?
            ORDER BY period
        """, (start_day, end_day))

    return [{'period': r[0], 'pv_kwh': r[1], 'grid_import_kwh': r[2],
             'grid_export_kwh': r[3], 'battery_charge_kwh': r[4],
             'battery_discharge_kwh': r[5],
             'consumption_kwh': r[1] + r[2] - r[3] - r[4] + r[5]} for r in cur.fetchall()]


def get_daily_data(analytics_conn, start_ts, end_ts):
    return get_period_data(analytics_conn, start_ts, end_ts)
