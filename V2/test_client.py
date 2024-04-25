import socket

HOST = 'localhost'
PORT = 8080

def receive_data():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")
        try:
            while True:
                data = s.recv(1024).decode()
                if not data:
                    break
                if data == "TRIGGER":
                    print("Sustained signal detected!")
                    # Perform desired action based on the "TRIGGER" message
                else:
                    print(f"Received message: {data}")
        except KeyboardInterrupt:
            print("Disconnecting from server...")

if __name__ == "__main__":
    receive_data()