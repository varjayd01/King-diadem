import secrets

from DATABASE.credit_store import add_credits
from DATABASE.user_store import create_user


api_keys = {}


def create_api_key():

    key = "kd_" + secrets.token_hex(16)

    api_keys[key] = {
        "credits": 100
    }

    # ให้เครดิตเริ่มต้น
    add_credits(key, 100)

    # สร้าง user
    create_user(key)

    return key


def is_valid_key(key):

    return key in api_keys
