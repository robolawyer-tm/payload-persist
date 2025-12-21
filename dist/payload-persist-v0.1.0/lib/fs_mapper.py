import os

def write_dict_to_fs(base_path, payload):
    for key, value in payload.items():
        current_path = os.path.join(base_path, key)
        if isinstance(value, dict):
            os.makedirs(current_path, exist_ok=True)
            write_dict_to_fs(current_path, value)
        elif isinstance(value, list):
            os.makedirs(base_path, exist_ok=True)
            file_path = current_path + ".txt"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(str(item) for item in value))
        else:
            os.makedirs(base_path, exist_ok=True)
            file_path = current_path + ".txt"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(str(value))

def read_fs_to_dict(base_path):
    result = {}
    if not os.path.exists(base_path):
        return result
        
    for entry in os.listdir(base_path):
        full_path = os.path.join(base_path, entry)
        if os.path.isdir(full_path):
            result[entry] = read_fs_to_dict(full_path)
        else:
            key = os.path.splitext(entry)[0]
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
            # Detect lists (multiple lines)
            if "\n" in content:
                result[key] = content.splitlines()
            else:
                result[key] = content
    return result
