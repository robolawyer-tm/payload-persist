def deep_update(data, path, value):
    """
    Updates a nested dictionary based on a dot-notation path.
    Autovivifies intermediate dictionaries if they don't exist.
    
    Args:
        data (dict): The dictionary to update.
        path (str): The dot-notation path (e.g., "a.b.c").
        value: The value to set at the path.
    """
    keys = path.split('.')
    current = data
    
    for i, key in enumerate(keys[:-1]):
        # If key doesn't exist, create it as a dict
        if key not in current:
            current[key] = {}
        
        # If key exists but isn't a dict, we can't traverse it
        if not isinstance(current[key], dict):
            raise TypeError(f"Cannot traverse path '{path}': '{key}' is not a dictionary.")
            
        current = current[key]
        
    # Set the value at the final key
    current[keys[-1]] = value
