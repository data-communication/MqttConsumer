# MQTT Consumer

An asynchronous Python application that subscribes to configured MQTT topics and displays incoming device measurements in a terminal dashboard. Updated measurements are briefly highlighted.

## Requirements

- Python 3.11 or later

## Setup

Create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a `.env` file in the project root with your broker settings:

```dotenv
MQTT_HOST=
MQTT_PORT=
MQTT_USERNAME=
MQTT_PASSWORD=
MQTT_TOPICS=
```

`MQTT_TOPICS` supports multiple topics separated by semicolon ';'. Wildcards are also supported.

## Run

With the virtual environment activated:

```powershell
python main.py
```

The application connects to the broker and prints incoming device measurements in the terminal. Stop it with `Ctrl+C`.

## Message format

Messages must be UTF-8 encoded JSON with a `deviceId` and a `measurements` array. Each measurement requires `type`, `value`, and `unit` fields. For example:

```json
{
  "deviceId": "sensor-01",
  "measurements": [
    {
      "type": "temperature",
      "value": 21.5,
      "unit": "°C"
    },
    {
      "type": "humidity",
      "value": 48,
      "unit": "%"
    }
  ]
}
```

## Project structure

```text
.
├── main.py                     # Loads configuration and starts the consumer
├── messaging/
│   └── mqtt_service.py          # MQTT connection, subscriptions, and dispatch
├── dashboard/
│   └── dashboard.py             # Terminal display for device measurements
├── requirements.txt
└── .env                         # Local broker configuration (create this)
```
