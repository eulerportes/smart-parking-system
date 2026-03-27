import requests
import random
import time
from datetime import datetime

URL = "http://127.0.0.1:5000/lpr"

PLATES = ["ABC1D23", "XYZ9K88", "BRA2E19", "QWE4R56"]


def send_event(plate, direction):
    payload = {
        "plate": plate,
        "confidence": round(random.uniform(85, 99), 2),
        "timestamp": datetime.now().isoformat(),
        "direction": direction,
        "device": "SIM_CAM_01"
    }

    response = requests.post(URL, json=payload, timeout=10)
    print(f"POST {payload} -> {response.status_code} {response.text}")


if __name__ == "__main__":
    while True:
        plate = random.choice(PLATES)
        direction = random.choice(["in", "out"])
        send_event(plate, direction)
        time.sleep(3)