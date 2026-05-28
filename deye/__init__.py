import os
from flask import Blueprint

bp = Blueprint('deye', __name__)

from . import routes  # noqa: F401


def create_app(config):
    from .inverter import Inverter
    app_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = config.get('db')
    if db_path and not os.path.isabs(db_path):
        db_path = os.path.join(app_dir, db_path)
    return Inverter(
        host=config.get('host'),
        port=config.get('port'),
        sn=config.get('sn'),
        db_path=db_path,
        interval=config.get('interval', 3),
    )
