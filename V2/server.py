import socket
import json
import time
from NeuroController import NeuroController

HOST = 'localhost'
PORT = 8080
SUSTAINED_SAMPLES = 5  # Number of samples required for sustained movement
TIME_WINDOW = 2  # Time window in seconds
PROBABILITY_THRESHOLD = 0.5  # Probability threshold for triggering
COOLDOWN_PERIOD = 5  # Cooldown period in seconds

def run_server():
    neuro_controller = NeuroController()
    neuro_controller.start_stream()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                sustained_count = 0
                start_time = time.time()
                trigger_sent = False
                last_trigger_time = 0

                while True:
                    latest_data = neuro_controller.get_latest_data()
                    if latest_data:
                        print(f"Latest data: {latest_data}")  # Print the latest data
                        if latest_data['label'] == 'leftFoot' and latest_data['confidence'] >= PROBABILITY_THRESHOLD:
                            sustained_count += 1
                            if sustained_count >= SUSTAINED_SAMPLES and time.time() - start_time <= TIME_WINDOW:
                                if not trigger_sent and time.time() - last_trigger_time > COOLDOWN_PERIOD:
                                    message = 'TRIGGER'
                                    conn.sendall(message.encode())
                                    trigger_sent = True
                                    last_trigger_time = time.time()
                        else:
                            sustained_count = 0
                            start_time = time.time()
                            trigger_sent = False

if __name__ == "__main__":
    run_server()