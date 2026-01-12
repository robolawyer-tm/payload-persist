#!/usr/bin/env python3
import sys
import json
from lib import crypto, network, protocol, utils

def store_secret(username, user_password, app_name, app_username, secret_text, passphrase):
    # Encrypt secret
    encrypted_data = crypto.encrypt_secret(secret_text, passphrase)
    if not encrypted_data.ok:
        print("Encryption failed:", encrypted_data.status)
        return

    message = protocol.create_store_payload(username, app_name, app_username, user_password, encrypted_data)

    with network.create_connection() as s:
        network.send_message(s, message.encode("utf-8"))
        ack = network.receive_message(s, 1024)
        print(f"Server response: {ack.decode()}")

def retrieve_secret(username, user_password, app_name, passphrase):
    request = protocol.create_retrieve_request(username, app_name, user_password)
    with network.create_connection() as s:
        network.send_message(s, request.encode("utf-8"))
        data = network.receive_message(s)

    if not data:
        print("No payload received.")
        return None

    decoded_data = data.decode("utf-8")
    if decoded_data.startswith("ERR:"):
        print(f"Server error: {decoded_data}")
        return None

    payload = json.loads(decoded_data)
    encrypted_text = payload["password"]
    app_username = payload.get("app_username", "N/A")

    decrypted_data = crypto.decrypt_secret(encrypted_text, passphrase)
    if decrypted_data.ok:
        print(f"Retrieved secret for {app_username}:", decrypted_data.data.decode())
        return decrypted_data.data.decode(), app_username
    else:
        print("Decryption failed:", decrypted_data.status)
        return None

def update_secret(username, user_password, app_name, passphrase, key_path, value):
    # 1. Retrieve existing secret
    print("Retrieving existing secret...")
    result = retrieve_secret(username, user_password, app_name, passphrase)
    if not result:
        print("Cannot update: Failed to retrieve or decrypt existing secret.")
        return

    current_json_str, app_username = result
    
    try:
        data = json.loads(current_json_str)
    except json.JSONDecodeError:
        # If it's not JSON, treat it as a raw string wrapped in a dict? 
        # Or just fail? For now, let's assume it's a dict or we make it one.
        print("Warning: Existing secret is not valid JSON. Overwriting with new structure.")
        data = {"raw_content": current_json_str}

    # 2. Apply update
    try:
        utils.deep_update(data, key_path, value)
    except TypeError as e:
        print(f"Update failed: {e}")
        return

    new_json_str = json.dumps(data, indent=2)
    print(f"Updated secret structure:\n{new_json_str}")

    # 3. Store updated secret
    print("Storing updated secret...")
    store_secret(username, user_password, app_name, app_username, new_json_str, passphrase)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  ./client.py store <username> <user_password> <app_name> <app_username> <passphrase> <secret_text>")
        print("  ./client.py retrieve <username> <user_password> <app_name> <passphrase>")
        print("  ./client.py update <username> <user_password> <app_name> <passphrase> <key_path> <value>")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "store":
        if len(sys.argv) < 8:
            print("Usage: ./client.py store <username> <user_password> <app_name> <app_username> <passphrase> <secret_text>")
            sys.exit(1)
        username = sys.argv[2]
        user_password = sys.argv[3]
        app_name = sys.argv[4]
        app_username = sys.argv[5]
        passphrase = sys.argv[6]
        secret_text = sys.argv[7]
        store_secret(username, user_password, app_name, app_username, secret_text, passphrase)

    elif command == "retrieve":
        if len(sys.argv) < 6:
            print("Usage: ./client.py retrieve <username> <user_password> <app_name> <passphrase>")
            sys.exit(1)
        username = sys.argv[2]
        user_password = sys.argv[3]
        app_name = sys.argv[4]
        passphrase = sys.argv[5]
        retrieve_secret(username, user_password, app_name, passphrase)

    elif command == "update":
        if len(sys.argv) < 8:
            print("Usage: ./client.py update <username> <user_password> <app_name> <passphrase> <key_path> <value>")
            sys.exit(1)
        username = sys.argv[2]
        user_password = sys.argv[3]
        app_name = sys.argv[4]
        passphrase = sys.argv[5]
        key_path = sys.argv[6]
        value = sys.argv[7]
        update_secret(username, user_password, app_name, passphrase, key_path, value)

    else:
        print("Unknown command. Use 'store', 'retrieve', or 'update'.")

