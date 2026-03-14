import os
import json
import threading
from pathlib import Path

DATA_DIR = Path("data")
DATA_FILE = DATA_DIR / "credits.json"

# thread lock ป้องกัน race condition
lock = threading.Lock()


# =========================
# INIT STORAGE
# =========================

def init_storage():

    DATA_DIR.mkdir(exist_ok=True)

    if not DATA_FILE.exists():
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)


# =========================
# LOAD DATA
# =========================

def load_data():

    init_storage()

    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return {}


# =========================
# SAFE SAVE
# =========================

def save_data(data):

    temp = DATA_FILE.with_suffix(".tmp")

    with open(temp, "w") as f:
        json.dump(data, f)

    os.replace(temp, DATA_FILE)


# =========================
# GET CREDITS
# =========================

def get_credits(api_key):

    with lock:

        data = load_data()

        return data.get(api_key, 0)


# =========================
# ADD CREDITS
# =========================

def add_credits(api_key, amount):

    with lock:

        data = load_data()

        current = data.get(api_key, 0)

        data[api_key] = current + amount

        save_data(data)


# =========================
# USE CREDIT
# =========================

def use_credit(api_key):

    with lock:

        data = load_data()

        current = data.get(api_key, 0)

        if current <= 0:
            return False

        data[api_key] = current - 1

        save_data(data)

        return True
