import json
import os
from flask import current_app, request, jsonify
from . import bp
from .inverter import ALL_REGISTERS

_script_dir = os.path.dirname(os.path.abspath(__file__))
_dashboard_path = os.path.join(_script_dir, 'dashboard.html')


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
