# Deye Inverter Monitor

Monitor a Deye SUN-6k-SG03LP1-EU hybrid solar inverter via Modbus/TCP over Ethernet.

## Architecture

Flask-based multi-app server. Each application lives in its own subdirectory with its own `config.json`, `__init__.py`, `routes.py`, and `inverter.py`. The dispatcher (`app.py`) auto-scans subdirectories, loads per-app config, and registers blueprints under `/{appname}`.

```
app.py              # Dispatcher (Flask server, blueprint auto-registration)
deye/               # PV monitor application
    config.json     # App-specific configuration
    __init__.py     # Blueprint + create_app()
    inverter.py     # Modbus polling, SQLite logging, Inverter class
    routes.py       # Flask routes
    dashboard.html  # Frontend template
```

To add a new app, create a subdirectory with `config.json`, `__init__.py` (defines `bp` and `create_app()`), and `routes.py`. It auto-registers under `/{dirname}`.

## Requirements

- Python 3.10+
- Network access to the inverter on port 8899 (Modbus TCP)

```
pip install -r requirements.txt
```

## Usage

```
python3 app.py
```

| Argument | Default | Description |
|---|---|---|
| `--http-host` | `0.0.0.0` | HTTP bind address |
| `--http-port` | `80` | HTTP port |

Configuration is per-app in each app's `config.json`:

```json
{
    "host": "192.168.1.2",
    "port": 8899,
    "sn": 3168400438,
    "interval": 3,
    "db": "test.db"
}
```

### Endpoints

| Path | Description |
|---|---|
| `/deye/` | Live dashboard (HTML) |
| `/deye/PV` | Latest readings as JSON |
| `/deye/api/readings?start=<ts>&end=<ts>` | Historical readings (Unix timestamps) |

## Register Map

| Register | Name | Unit |
|---|---|---|
| 79 | Grid Frequency | Hz |
| 109 | PV1 Voltage | V |
| 110 | PV1 Current | A |
| 111 | PV2 Voltage | V |
| 112 | PV2 Current | A |
| 150 | Grid Voltage | V |
| 154 | Inverter Voltage | V |
| 157 | Load Voltage L1 | V |
| 160 | Grid Current L | A |
| 161 | Grid Current N | A |
| 164 | Inverter Current | A |
| 166 | AUX Power | W |
| 169 | Grid Power | W |
| 172 | Grid CT Power | W |
| 175 | Inverter Power | W |
| 176 | Load Power L1 | W |
| 178 | Load Power Total | W |
| 179 | Load Current L1 | A |
| 181 | AUX Voltage | V |
| 182 | Battery Temp | °C |
| 183 | Battery Voltage | V |
| 184 | Battery SOC | % |
| 186 | PV1 Power | W |
| 187 | PV2 Power | W |
| 190 | Battery Power | W |
| 191 | Battery Current | A |
| 192 | Load Frequency | Hz |
| 193 | Inverter Freq | Hz |
| 196 | AUX Frequency | Hz |
| 314 | Batt Charge Limit | A |
| 315 | Batt Discharge Limit | A |

## Disclaimer

This project was created by the Qwen 3.6 large language model. It is provided as-is without warranty. Use at your own risk — verify all Modbus register addresses and scales against your inverter's official documentation before deploying.
