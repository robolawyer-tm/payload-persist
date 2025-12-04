#!/usr/bin/env python3
import os
import sys
import gnupg
import socket
import json
import datetime

HOST = "127.0.0.1"
PORT = 65432

gpg = gnupg.GPG(gnupghome=os.path.expanduser("~/.gnupg"))

def store_secret(app_name, secret_text, passphrase):
    # Encrypt secret
    encrypted_data = gpg.encrypt(
        secret_text,
        recipients=None,
        symmetric=True,
        passphrase=passphrase
    )
    if not encrypted_data.ok:
        print("Encryption failed:", encrypted_data.status)
        return

    payload = {
        "secret": str(encrypted_data),
        "timestamp": datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    }
    message = json.dumps({"app": app_name, "payload": payload})

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(message.encode("utf-8"))
        ack = s.recv(1024)
        print(f"Server response: {ack.decode()}")

def retrieve_secret(app_name, passphrase):
    request = json.dumps({"command": "REQUEST_SECRET", "app": app_name})
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(request.encode("utf-8"))
        data = s.recv(8192)

    if not data:
        print("No payload received.")
        return

    payload = json.loads(data.decode("utf-8"))
    encrypted_text = payload["secret"]

    decrypted_data = gpg.decrypt(encrypted_text, passphrase=passphrase)
    if decrypted_data.ok:
        print("Retrieved secret:", decrypted_data.data.decode())
    else:
        print("Decryption failed:", decrypted_data.status)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  ./client.py store <app_name> <secret_text> <passphrase>")
        print("  ./client.py retrieve <app_name> <passphrase>")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "store":
        if len(sys.argv) < 5:
            print("Usage: ./client.py store <app_name> <secret_text> <passphrase>")
            sys.exit(1)
        app_name = sys.argv[2]
        secret_text = sys.argv[3]
        passphrase = sys.argv[4]
        store_secret(app_name, secret_text, passphrase)

    elif command == "retrieve":
        if len(sys.argv) < 4:
            print("Usage: ./client.py retrieve <app_name> <passphrase>")
            sys.exit(1)
        app_name = sys.argv[2]
        passphrase = sys.argv[3]
        retrieve_secret(app_name, passphrase)

    else:
        print("Unknown command. Use 'store' or 'retrieve'.")

