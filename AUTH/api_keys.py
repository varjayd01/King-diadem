import secrets

from DATABASE.credit_store import add_credits

api_keys = {}


def create_api_key():

    key = "kd_" + secrets.token_hex(16)

    api_keys[key] = {
        "credits": 100
    }

    add_credits(key, 100)

    return key


def is_valid_key(key):

    return key in api_keys
