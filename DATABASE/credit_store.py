import threading

credits = {}

lock = threading.Lock()


def get_credits(api_key):

    with lock:

        if api_key not in credits:
            return 0

        return credits[api_key]


def add_credits(api_key, amount):

    with lock:

        if api_key not in credits:
            credits[api_key] = 0

        credits[api_key] += amount

        return credits[api_key]


def use_credit(api_key):

    with lock:

        if api_key not in credits:
            return False

        if credits[api_key] <= 0:
            return False

        credits[api_key] -= 1

        return True
