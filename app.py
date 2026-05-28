#!/usr/bin/env python3
"""Deye inverter monitor - Flask multi-app server."""
import os
import sys
import json
import signal
import importlib
import pkgutil

_script_dir = os.path.dirname(os.path.abspath(__file__))
_venv = os.path.join(_script_dir, 'venv')
if os.path.isdir(_venv):
    for entry in os.listdir(os.path.join(_venv, 'lib')):
        sp = os.path.join(_venv, 'lib', entry, 'site-packages')
        if os.path.isdir(sp):
            sys.path.insert(0, sp)
            break

from flask import Flask

app = Flask(__name__, template_folder=None)

# Global state
_apps = {}


def shutdown(signum, frame):
    print("\n\nStopped.")
    for name, obj in _apps.items():
        if hasattr(obj, 'stop'):
            obj.stop()
    sys.exit(0)


def register_blueprints():
    """Auto-discover and register blueprints from sibling app directories."""
    for importer, modname, ispkg in pkgutil.iter_modules([_script_dir]):
        if modname in ('app',):
            continue
        try:
            mod = importlib.import_module(f'{modname}')
            if hasattr(mod, 'bp'):
                app.register_blueprint(mod.bp, url_prefix=f'/{modname}')
                print(f"Registered app: {modname}")
        except Exception as e:
            print(f"Failed to register {modname}: {e}")


def load_app_config(app_dir):
    """Load config.json from an app directory."""
    config_path = os.path.join(app_dir, 'config.json')
    if os.path.isfile(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    return {}


register_blueprints()

# Create app instances from per-app config files
for importer, modname, ispkg in pkgutil.iter_modules([_script_dir]):
    if modname in ('app',):
        continue
    try:
        mod = importlib.import_module(f'{modname}')
        if not hasattr(mod, 'create_app'):
            continue
        app_dir = os.path.join(_script_dir, modname)
        app_config = load_app_config(app_dir)
        obj = mod.create_app(app_config)
        _apps[modname] = obj
        app.extensions[modname] = obj
        if hasattr(obj, 'connect'):
            obj.connect()
        if hasattr(obj, 'start'):
            obj.start()
        print(f"Started app: {modname}")
    except Exception as e:
        print(f"Failed to start {modname}: {e}")

signal.signal(signal.SIGINT, shutdown)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Deye inverter monitor - Flask multi-app server"
    )
    parser.add_argument("--http-host", default="0.0.0.0",
                        help="HTTP bind address (default: 0.0.0.0)")
    parser.add_argument("--http-port", type=int, default=80,
                        help="HTTP port (default: 80)")
    args = parser.parse_args()

    http_host = args.http_host
    http_port = args.http_port

    try:
        app.run(host=http_host, port=http_port, threaded=True)
    except PermissionError:
        print(f"ERROR: Permission denied binding to port {http_port}.")
        print(f"  Port 80 requires root privileges. Run with sudo:")
        print(f"    sudo python3 app.py --http-port 8080")
        sys.exit(1)
    except OSError as e:
        print(f"ERROR: Cannot bind to port {http_port}: {e}")
        print(f"  Another service may already be using this port.")
        print(f"  Use --http-port to specify a different port.")
        sys.exit(1)
