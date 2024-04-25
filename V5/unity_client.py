import socket
import json
import time
import requests
from NeuroController import NeuroController
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

HOST = 'localhost'
PORT = 8080
COOLDOWN_PERIOD = 5  # seconds
is_on = False


def send_data_to_server(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        json_data = json.dumps(data)  # Convert data to JSON string
        s.sendall(json_data.encode())
        print(f"Sent to server: {json_data}")


def main():
    global is_on
    neuro_controller = NeuroController()
    neuro_controller.start_stream("leftArm")
    last_send_time = time.time() - COOLDOWN_PERIOD

    try:
        while True:
            data = neuro_controller.get_latest_data()
            if data:
                probability = data.get('predictions', [{}])[0].get('probability', 0)
                if probability > 0.9 and time.time() - last_send_time >= COOLDOWN_PERIOD:
                    if is_on == False:
                        is_on = True
                        continue
                    
                    json_data = {
                        "label": data['label'],
                        "probability": probability,
                        "timestamp": data.get('predictions', [{}])[0].get('timestamp', 0)
                    }
                    send_data_to_server(json_data)
                    last_send_time = time.time()
            time.sleep(1)  # Reduce CPU usage by waiting between checks
    finally:
        neuro_controller.stop_stream()

if __name__ == "__main__":
    main()