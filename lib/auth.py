import os
import json
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = kdf.derive(password.encode())
    return key, salt

def verify_password(stored_hash_b64, stored_salt_b64, password_input):
    salt = base64.b64decode(stored_salt_b64)
    derived_key, _ = hash_password(password_input, salt)
    stored_key = base64.b64decode(stored_hash_b64)
    return derived_key == stored_key

def save_auth(username, password):
    auth_dir = os.path.join("db", username)
    os.makedirs(auth_dir, exist_ok=True)
    
    auth_file = os.path.join(auth_dir, "auth.json")
    
    # Generate new hash
    key, salt = hash_password(password)
    
    # Store as base64
    data = {
        "hash": base64.b64encode(key).decode('utf-8'),
        "salt": base64.b64encode(salt).decode('utf-8'),
        "method": "pbkdf2:sha256:100000"
    }
    
    with open(auth_file, "w") as f:
        json.dump(data, f)
    return True

def check_auth(username, password):
    auth_file = os.path.join("db", username, "auth.json")
    if not os.path.exists(auth_file):
        return False # User does not exist
        
    try:
        with open(auth_file, "r") as f:
            data = json.load(f)
        
        # Backward compatibility check (migrating old users could go here, but for now we just fail safe)
        if "salt" not in data:
            return False 
            
        return verify_password(data["hash"], data["salt"], password)
    except Exception:
        return False
