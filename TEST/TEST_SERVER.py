import socket

HOST = 'localhost'  # Standard loopback interface address (localhost)
PORT = 8080         # Port to listen on (non-privileged ports are > 1023)

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Test server listening on {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    message = data.decode()
                    print(f"Message received: {message}")

if __name__ == "__main__":
    start_server()
