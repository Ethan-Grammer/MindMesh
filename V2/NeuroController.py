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

    def kinesis_callback(self, data):
        if data['label'] == 'leftFoot':
            print('leftFoot')
            self.latest_data = data

    def start_stream(self):
        self.unsubscribe = self.neurosity.kinesis("leftFoot", self.kinesis_callback)

    def stop_stream(self):
        if self.unsubscribe:
            self.unsubscribe()

    def get_latest_data(self):
        return self.latest_data