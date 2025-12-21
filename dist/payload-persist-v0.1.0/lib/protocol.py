import json
import datetime

def create_store_payload(username, app_name, app_username, user_password, encrypted_secret):
    payload = {
        "app_username": app_username,
        "password": str(encrypted_secret),
        "timestamp": datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    }
    return json.dumps({
        "username": username,
        "user_password": user_password,
        "app": app_name,
        "payload": payload
    })

def create_retrieve_request(username, app_name, user_password):
    return json.dumps({
        "command": "REQUEST_SECRET",
        "username": username,
        "user_password": user_password,
        "app": app_name
    })

def parse_message(data_bytes):
    if not data_bytes:
        return None
    return json.loads(data_bytes.decode("utf-8"))
