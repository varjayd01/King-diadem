import uuid
import json
import os

API_KEY_FILE = "data/api_keys.json"


def load_keys():
    if not os.path.exists(API_KEY_FILE):
        return {}

    with open(API_KEY_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return {}


def save_keys(keys):
    with open(API_KEY_FILE, "w") as f:
        json.dump(keys, f, indent=2)


def create_api_key(user="public"):
    keys = load_keys()

    key = str(uuid.uuid4())

    keys[key] = {
        "user": user,
        "usage": 0
    }

    save_keys(keys)

    return key


def validate_api_key(key):
    keys = load_keys()

    if key in keys:
        keys[key]["usage"] += 1
        save_keys(keys)
        return True

    return False
