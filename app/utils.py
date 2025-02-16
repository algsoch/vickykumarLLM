import json

def save_json(filepath, data):
    """Saves data to a JSON file."""
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

def load_json(filepath):
    """Loads data from a JSON file."""
    with open(filepath, "r") as f:
        return json.load(f)
