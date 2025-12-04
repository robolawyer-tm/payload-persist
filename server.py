import socket
import os
import json

HOST = "127.0.0.1"
PORT = 65432

def handle_store(app_name, payload, conn):
    # Ensure directory exists
    os.makedirs(app_name, exist_ok=True)

    # Filename with timestamp
    filename = os.path.join(app_name, f"backup-{payload['timestamp']}.json")

    # Save payload
    with open(filename, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"Stored payload in {filename}")
    conn.sendall(b"ACK: Payload stored")

def handle_retrieve(app_name, conn):
    if not os.path.exists(app_name):
        conn.sendall(b"")
        return

    files = sorted(os.listdir(app_name))
    if not files:
        conn.sendall(b"")
        return

    latest = os.path.join(app_name, files[-1])
    with open(latest, "r") as f:
        data = f.read()

    print(f"Sent payload from {latest}")
    conn.sendall(data.encode("utf-8"))

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}...")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(8192)
                if not data:
                    continue

                try:
                    message = json.loads(data.decode("utf-8"))

                    if message.get("command") == "REQUEST_SECRET":
                        app_name = message["app"]
                        handle_retrieve(app_name, conn)
                    else:
                        app_name = message["app"]
                        payload = message["payload"]
                        handle_store(app_name, payload, conn)

                except Exception as e:
                    print("Error:", e)
                    conn.sendall(b"ERR: Failed to process request")

if __name__ == "__main__":
    main()

