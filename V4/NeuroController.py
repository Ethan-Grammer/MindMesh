from neurosity import NeurositySDK
from dotenv import load_dotenv
import os

class NeuroController:
    def __init__(self):
        load_dotenv()
        self.neurosity = NeurositySDK({"device_id": os.getenv("NEUROSITY_DEVICE_ID")})
        self.neurosity.login({
            "email": os.getenv("NEUROSITY_EMAIL"),
            "password": os.getenv("NEUROSITY_PASSWORD")
        })
        self.unsubscribe = None
        self.latest_data = None
        self.last_timestamp = 0  # Store the last timestamp to filter old data

    def kinesis_callback(self, data):
        # Only update if the data is newer than what we've already processed
        current_timestamp = data.get('timestamp', 0)
        if current_timestamp > self.last_timestamp:
            self.last_timestamp = current_timestamp
            self.latest_data = data
            print(f"Received data: {data}")  # Print all incoming data for monitoring

    def start_stream(self, label):
        self.unsubscribe = self.neurosity.kinesis(label, self.kinesis_callback)

    def stop_stream(self):
        if self.unsubscribe:
            self.unsubscribe()

    def get_latest_data(self):
        # Return the latest data and reset it to prevent multiple sends of the same data
        temp_data = self.latest_data
        self.latest_data = None
        return temp_data
