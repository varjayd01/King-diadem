import uuid
import json
import os

API_KEY_FILE = "data/api_keys.json"


# -----------------------------
# LOAD API KEYS
# -----------------------------
def load_keys():

    if not os.path.exists(API_KEY_FILE):
        return {}

    try:
        with open(API_KEY_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


# -----------------------------
# SAVE API KEYS
# -----------------------------
def save_keys(keys):

    os.makedirs("data", exist_ok=True)

    with open(API_KEY_FILE, "w") as f:
        json.dump(keys, f, indent=2)


# -----------------------------
# CREATE NEW API KEY
# -----------------------------
def create_api_key(user="public"):

    keys = load_keys()

    key = str(uuid.uuid4())

    keys[key] = {
        "user": user,
        "usage": 0
    }

    save_keys(keys)

    return key


# -----------------------------
# VALIDATE API KEY
# -----------------------------
def validate_api_key(key=None):

    # 🔑 DEVELOPMENT MODE
    # อนุญาตทุก request เพื่อให้เว็บทำงานก่อน
    return True
