import json
import os
import time
from datetime import datetime, timezone
from flask import current_app, request, jsonify
from . import bp
from .inverter import ALL_REGISTERS
from . import analytics as analytics_mod

_script_dir = os.path.dirname(os.path.abspath(__file__))
_dashboard_path = os.path.join(_script_dir, 'dashboard.html')
_analytics_path = os.path.join(_script_dir, 'analytics.html')


@bp.route('/')
def dashboard():
    with open(_dashboard_path, 'r') as f:
        html = f.read()
    return html


@bp.route('/PV')
def pvstate():
    inverter = current_app.extensions['deye']
    data = inverter.get_data()
    return jsonify(data or {})


@bp.route('/api/readings')
def api_readings():
    inverter = current_app.extensions['deye']
    db_conn = inverter.get_db_conn()
    if not db_conn:
        return jsonify({"error": "Database not configured"}), 503

    params = request.args
    start = params.get('start')
    end = params.get('end')
    if not start or not end:
        return jsonify({"error": "start and end parameters required"}), 400

    start = int(start)
    end = int(end)
    try:
        col_names_str = ', '.join([f'`{r[1]}`' for r in ALL_REGISTERS])
        sql = f"SELECT timestamp, {col_names_str} FROM readings WHERE timestamp >= ? AND timestamp <= ? ORDER BY timestamp"
        cur = db_conn.cursor()
        cur.execute(sql, (start, end))
        rows = cur.fetchall()
        if not rows:
            return jsonify([])
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
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def _get_time_range():
    params = request.args
    start = params.get('start')
    end = params.get('end')
    if not start or not end:
        return None, None
    return int(start), int(end)


def _get_range_params():
    range_val = request.args.get('range', 'month')
    now = datetime.fromtimestamp(time.time(), tz=timezone.utc)
    if range_val == 'week':
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        days_since_monday = start.weekday()
        start = start.replace(day=start.day - days_since_monday)
        start = int(start.timestamp())
        end = int(now.timestamp())
    elif range_val == 'month':
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        start = int(start.timestamp())
        end = int(now.timestamp())
    elif range_val == 'year':
        start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        start = int(start.timestamp())
        end = int(now.timestamp())
    elif range_val == 'lifetime':
        start = 0
        end = int(now.timestamp())
    elif range_val == 'custom':
        start, end = _get_time_range()
    else:
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        start = int(start.timestamp())
        end = int(now.timestamp())
    return start, end


@bp.route('/analytics')
def analytics_page():
    with open(_analytics_path, 'r') as f:
        html = f.read()
    return html


@bp.route('/api/analytics/period')
def api_analytics_period():
    inverter = current_app.extensions['deye']
    if not hasattr(inverter, 'analytics_conn') or not inverter.analytics_conn:
        return jsonify({"error": "Analytics not configured"}), 503
    start, end = _get_range_params()
    totals = analytics_mod.get_period_totals(inverter.analytics_conn, start, end)
    num_days = max(1, (end - start) / 86400)
    totals['daily_avg_pv_kwh'] = round(totals['pv_kwh'] / num_days, 4)
    totals['daily_avg_grid_import_kwh'] = round(totals['grid_import_kwh'] / num_days, 4)
    totals['daily_avg_consumption_kwh'] = round(totals['consumption_kwh'] / num_days, 4)
    return jsonify(totals)


@bp.route('/api/analytics/daily')
def api_analytics_daily():
    inverter = current_app.extensions['deye']
    if not hasattr(inverter, 'analytics_conn') or not inverter.analytics_conn:
        return jsonify({"error": "Analytics not configured"}), 503
    start, end = _get_range_params()
    daily = analytics_mod.get_daily_data(inverter.analytics_conn, start, end)
    return jsonify(daily)


@bp.route('/api/analytics/period_data')
def api_analytics_period_data():
    inverter = current_app.extensions['deye']
    if not hasattr(inverter, 'analytics_conn') or not inverter.analytics_conn:
        return jsonify({"error": "Analytics not configured"}), 503
    start, end = _get_range_params()
    range_val = request.args.get('range', 'month')
    data = analytics_mod.get_period_data(inverter.analytics_conn, start, end, range_val)
    return jsonify(data)


@bp.route('/api/analytics/lifetime')
def api_analytics_lifetime():
    inverter = current_app.extensions['deye']
    if not hasattr(inverter, 'analytics_conn') or not inverter.analytics_conn:
        return jsonify({"error": "Analytics not configured"}), 503
    cur = inverter.analytics_conn.execute("""
        SELECT
            COALESCE(SUM(pv_kwh), 0) as pv_kwh,
            COALESCE(SUM(grid_import_kwh), 0) as grid_import_kwh,
            COALESCE(SUM(grid_export_kwh), 0) as grid_export_kwh,
            COALESCE(SUM(battery_charge_kwh), 0) as battery_charge_kwh,
            COALESCE(SUM(battery_discharge_kwh), 0) as battery_discharge_kwh
        FROM day_agg
    """)
    row = cur.fetchone()
    pv = row[0]
    gi = row[1]
    ge = row[2]
    bc = row[3]
    bd = row[4]
    consumption = pv + gi - ge - bc + bd
    return jsonify({
        'pv_kwh': round(pv, 4),
        'grid_import_kwh': round(gi, 4),
        'consumption_kwh': round(consumption, 4),
    })
