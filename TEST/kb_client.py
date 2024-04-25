import socket
import json
import time
from pynput import keyboard

HOST = 'localhost'  # The server's hostname or IP address
PORT = 8080         # The port used by the server

def send_json_data(key):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        message = json.dumps({"key": key})
        s.sendall(message.encode())

class KeyboardController:
    def __init__(self):
        self.key_start_time = {}

    def on_press(self, key):
        try:
            if key in [keyboard.Key.f1, keyboard.Key.f2]:
                self.key_start_time[key] = time.time()
                print(f"{key} pressed")  # Print on key press
        except AttributeError:
            # This will pass if the key is not recognized (for example, a special key)
            pass

    def on_release(self, key):
        try:
            if key in [keyboard.Key.f1, keyboard.Key.f2]:
                duration = time.time() - self.key_start_time.get(key, 0)
                action = "HOLD" if duration >= 2 else "PRESS"
                print(f"{key} released after {duration:.2f} seconds ({action})")  # Print on key release
                send_json_data(f"{key}_{action}")
        except AttributeError:
            # This will pass if the key is not recognized
            pass

    def start(self):
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.keyboard_listener.start()

    def stop(self):
        if self.keyboard_listener:
            self.keyboard_listener.stop()

if __name__ == "__main__":
    controller = KeyboardController()
    controller.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        controller.stop()
        print("Program exiting gracefully...")
