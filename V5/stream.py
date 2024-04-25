import time
from NeuroController import NeuroController

def stream_data(label, neuro_controller):
    neuro_controller.start_stream(label)

    try:
        while True:
            data = neuro_controller.get_latest_data()
            if data:
                predicted_label = data.get('label', 'Unknown')
                probability = data.get('predictions', [{}])[0].get('probability', 0)
                print(f"Stream: {label}, Label: {predicted_label}, Probability: {probability}")
            time.sleep(1)  # Reduce CPU usage by waiting between checks
    finally:
        neuro_controller.stop_stream()

def main():
    import threading

    # Create NeuroController instances in the main thread
    neuro_controller1 = NeuroController()
    neuro_controller2 = NeuroController()

    # Create separate threads for each label, passing the NeuroController instances
    thread1 = threading.Thread(target=stream_data, args=("bitingALemon", neuro_controller1))
    thread2 = threading.Thread(target=stream_data, args=("rightArm", neuro_controller2))

    # Start both threads
    thread1.start()
    thread2.start()

    # Wait for both threads to complete
    thread1.join()
    thread2.join()

if __name__ == "__main__":
    main()