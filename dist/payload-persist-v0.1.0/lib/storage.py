import os
import json
from . import auth

def store_payload(username, app_name, user_password, payload):
    # Authenticate / Register
    if not auth.save_auth(username, user_password):
        raise PermissionError("Authentication failed")

    # Ensure directory exists: db/username/app_name
    dir_path = os.path.join("db", username, app_name)
    os.makedirs(dir_path, exist_ok=True)

    # Fixed filename
    filename = os.path.join(dir_path, "secret.json")

    # Save payload
    with open(filename, "w") as f:
        json.dump(payload, f, indent=2)
    
    return filename

def retrieve_latest_payload(username, app_name, user_password):
    # Authenticate
    if not auth.check_auth(username, user_password):
        raise PermissionError("Authentication failed")

    # Path: db/username/app_name/secret.json
    file_path = os.path.join("db", username, app_name, "secret.json")
    
    if not os.path.exists(file_path):
        return None

    with open(file_path, "r") as f:
        data = f.read()
    
    return data, file_path
