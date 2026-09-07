import subprocess
import sys
import time
from pathlib import Path

COMMANDS = [
    ("gateway", "api_gateway.main:app", 8000),
    ("hotel", "hotel_service.app.main:app", 8001),
    ("room", "room_service.app.main:app", 8002),
    ("reservation", "reservation_service.app.main:app", 8003),
    ("review", "review_service.app.main:app", 8004),
    ("user", "user_service.app.main:app", 8005),
    ("notification", "notification_service.app.main:app", 8006),
]

processes = []

print("Pornesc serviciile FastAPI. Închidere: CTRL+C")

try:
    for name, app, port in COMMANDS:
        cmd = [
            sys.executable,
            "-m",
            "uvicorn",
            app,
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ]

        print(f"{name}: http://127.0.0.1:{port}/docs")
        process = subprocess.Popen(cmd, cwd=Path(__file__).parent)
        processes.append(process)

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Oprire servicii...")
    for process in processes:
        process.terminate()
