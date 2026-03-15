from DATABASE.user_db import add_credit


def topup(email, amount):

    add_credit(email, amount)

    return {
        "status": "success",
        "added": amount
    }
