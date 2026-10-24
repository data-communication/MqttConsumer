import json
import sys
import asyncio

class Dashboard:
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RESET = "\033[0m"

    def __init__(self):
        print("\033[2J\033[H", end="")

        self.anchor_row = 2
        self.device_rows = {}
        self.last_measurements = {}

    def move_cursor(self, relative_row: int):
        print(f"\033[{self.anchor_row + relative_row};1H", end="")

    def clear_line(self):
        print("\033[2K", end="")

    async def update(self, device_id: str, measurements: dict):
        if device_id not in self.device_rows:
            self.device_rows[device_id] = len(self.device_rows)

        row = self.device_rows[device_id]
        old = self.last_measurements.get(device_id, [])

        segments = []
        for i, m in enumerate(measurements):
            text = f"{m['type']}: {m['value']} {m['unit']}"
            changed = (i >= len(old)) or (old[i] != m)
            color = self.YELLOW if changed else self.RESET
            segments.append((color, text))

        self.move_cursor(row)
        self.clear_line()

        print(f"{self.GREEN}{device_id}{self.RESET}: ", end="")
        for color, text in segments:
            print(f"{color}{text}{self.RESET} | ", end="")
        sys.stdout.flush()

        await asyncio.sleep(0.250)

        self.move_cursor(row)
        self.clear_line()

        print(f"{self.GREEN}{device_id}{self.RESET}: ", end="")
        for _, text in segments:
            print(f"{self.RESET}{text}{self.RESET} | ", end="")
        sys.stdout.flush()

        self.last_measurements[device_id] = measurements
        self.move_cursor(len(self.device_rows)+1)

    async def handle_message(self, payload: str):
        try:
            data = json.loads(payload)
            device_id = data["deviceId"]
            measurements = data["measurements"]
            await self.update(device_id, measurements)
        except Exception as ex:
            print(ex)
