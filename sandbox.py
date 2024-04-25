from neurosity import NeurositySDK
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Neurosity SDK with device ID
neurosity = NeurositySDK({
    "device_id": os.getenv("NEUROSITY_DEVICE_ID")
})

# Log into the Neurosity SDK
neurosity.login({
    "email": os.getenv("NEUROSITY_EMAIL"),
    "password": os.getenv("NEUROSITY_PASSWORD")
})

# Callback function that gets called with new Kinesis data
def kinesis_callback(data):
    if data['label'] == 'leftFoot':
        print('leftFoot')

def main():
    # Subscribe to the Kinesis metric for left arm movement
    unsubscribe = neurosity.kinesis("leftFoot", kinesis_callback)

    try:
        # Keep the application running to continuously receive data
        print("Waiting for left arm movement...")
        input("Press Enter to stop...\n")
    finally:
        # Unsubscribe when done to clean up resources
        unsubscribe()

if __name__ == "__main__":
    main()