import os
from flask import Blueprint

bp = Blueprint('deye', __name__)


def create_app(config):
    from . import routes  # noqa: F401
    from .inverter import Inverter
    from . import analytics as analytics_mod
    app_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = config.get('db')
    if db_path and not os.path.isabs(db_path):
        db_path = os.path.join(app_dir, db_path)
    inverter = Inverter(
        host=config.get('host'),
        port=config.get('port'),
        sn=config.get('sn'),
        db_path=db_path,
        interval=config.get('interval', 3),
    )
    analytics_db_path = config.get('analytics_db')
    if analytics_db_path and not os.path.isabs(analytics_db_path):
        analytics_db_path = os.path.join(app_dir, analytics_db_path)
    if analytics_db_path:
        inverter.analytics_conn = analytics_mod.init_analytics(analytics_db_path)
        inverter._analytics_update = lambda ts, readings: analytics_mod.update_analytics(inverter.analytics_conn, ts, readings)
    else:
        inverter._analytics_update = None
    return inverter
