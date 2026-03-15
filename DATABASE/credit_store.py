credits = {
    "test123": 100
}


def get_credits(api_key):
    return credits.get(api_key, 0)


def use_credit(api_key):

    if api_key not in credits:
        return False

    if credits[api_key] <= 0:
        return False

    credits[api_key] -= 1
    return True


def add_credits(api_key, amount):

    if api_key not in credits:
        credits[api_key] = 0

    credits[api_key] += amount
