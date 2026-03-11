import json
import os
import uuid
import hashlib

USERS_FILE = "data/users.json"


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}

    with open(USERS_FILE) as f:
        return json.load(f)


def save_users(users):
    os.makedirs("data", exist_ok=True)

    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def create_user(email, password):

    users = load_users()

    if email in users:
        return None

    api_key = "kd_" + uuid.uuid4().hex

    users[email] = {
        "password": hash_password(password),
        "credits": 10,
        "api_key": api_key
    }

    save_users(users)

    return api_key


def authenticate_user(email, password):

    users = load_users()

    if email not in users:
        return None

    if users[email]["password"] != hash_password(password):
        return None

    return users[email]["api_key"]
