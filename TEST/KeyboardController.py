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
        if key in [keyboard.Key.f1, keyboard.Key.f2]:
            self.key_start_time[key] = time.time()

    def on_release(self, key):
        if key in [keyboard.Key.f1, keyboard.Key.f2]:
            duration = time.time() - self.key_start_time.get(key, 0)
            if duration >= 2:
                send_json_data(f"{key}_HOLD")
            else:
                send_json_data(f"{key}_PRESS")

    def start(self):
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.keyboard_listener.start()
        self.keyboard_listener.join()  # Wait for the listener thread to exit

    def stop(self):
        if self.keyboard_listener:
            self.keyboard_listener.stop()

if __name__ == "__main__":
    controller = KeyboardController()
    controller.start()
