import socket
import json
import time
import requests
from NeuroController import NeuroController
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

LIGHT_BULB_SERVER_URL = f'http://localhost:8081'  # URL of the light bulb server
COOLDOWN_PERIOD = 5  # seconds

is_light_on = False  # Initialize the light state to False (off)
on_start = False

def send_data_to_server(data):

    global is_light_on

    if not is_light_on:
        # Send a POST request to the /on endpoint of the light bulb server
        response = requests.post(f"{LIGHT_BULB_SERVER_URL}/on")
        if response.status_code == 200:
            print("Light bulb turned on")
            is_light_on = True
        else:
            print("Failed to turn on the light bulb")
    else:
        # Send a POST request to the /off endpoint of the light bulb server
        response = requests.post(f"{LIGHT_BULB_SERVER_URL}/off")
        if response.status_code == 200:
            print("Light bulb turned off")
            is_light_on = False
        else:
            print("Failed to turn off the light bulb")

def main():
    neuro_controller = NeuroController()
    neuro_controller.start_stream("leftArm")
    last_send_time = time.time() - COOLDOWN_PERIOD

    global on_start
    
    try:
        while True:
            data = neuro_controller.get_latest_data()
            if data:
                probability = data.get('predictions', [{}])[0].get('probability', 0)
                if probability > 0.9 and time.time() - last_send_time >= COOLDOWN_PERIOD:
                    if on_start == False:
                        on_start = True
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