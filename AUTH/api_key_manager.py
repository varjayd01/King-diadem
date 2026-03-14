import uuid

API_KEYS = {
    "KING-001": {"credits":10}
}

def generate_api_key():
    key = "KD-" + str(uuid.uuid4())[:8]
    API_KEYS[key] = {"credits":10}
    return key

def validate_api_key(key):
    return key in API_KEYS

def use_credit(key):
    if API_KEYS[key]["credits"] <= 0:
        return False
    API_KEYS[key]["credits"] -= 1
    return True

def add_credit(key, amount):
    API_KEYS[key]["credits"] += amount
