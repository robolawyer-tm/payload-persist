import hashlib
import os
import json

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_hash, password):
    return stored_hash == hash_password(password)

def save_auth(username, password):
    auth_dir = os.path.join("db", username)
    os.makedirs(auth_dir, exist_ok=True)
    
    auth_file = os.path.join(auth_dir, "auth.json")
    
    # If auth file exists, verify password
    if os.path.exists(auth_file):
        with open(auth_file, "r") as f:
            data = json.load(f)
        if not verify_password(data["hash"], password):
            return False
        return True
    
    # If not exists, create it (Registration)
    data = {"hash": hash_password(password)}
    with open(auth_file, "w") as f:
        json.dump(data, f)
    return True

def check_auth(username, password):
    auth_file = os.path.join("db", username, "auth.json")
    if not os.path.exists(auth_file):
        return False # User does not exist
        
    with open(auth_file, "r") as f:
        data = json.load(f)
    return verify_password(data["hash"], password)
