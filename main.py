import asyncio
import sys
import os
import json

from dotenv import load_dotenv

from messaging.mqtt_service import MqttService
from dashboard.dashboard import Dashboard

async def handle_message(payload, dashboard: Dashboard):
    try:
        data = json.loads(payload)
        device_id = data.get("deviceId") or data.get("id") or "unknown"
        dashboard.update(device_id, data)
    except Exception:
        print("Invalid MQTT telemetry payload")

async def main():
    load_dotenv()

    dashboard = Dashboard()

    mqtt_service = MqttService(
        host=os.getenv("MQTT_HOST", "localhost"),
        port=int(os.getenv("MQTT_PORT", "1883")),
        username=os.getenv("MQTT_USERNAME"),
        password=os.getenv("MQTT_PASSWORD"),
        identifier="Mqtt-Consumer"
    )

    topics = [
        topic.strip()
        for topic in os.getenv("MQTT_TOPICS").split(";")
        if topic.strip()
    ]

    for topic in topics:
        mqtt_service.register(topic, dashboard.handle_message)

    try:
        async with asyncio.TaskGroup() as tasks:
            tasks.create_task(mqtt_service.run())
    except asyncio.CancelledError:
        print("\033[?25h", end="")
        print("Shutting down.")


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.run(main(), loop_factory=asyncio.SelectorEventLoop)
    else:
        asyncio.run(main())