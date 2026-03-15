from DATABASE.user_db import create_user, get_user


def register(email, password):

    success = create_user(email, password)

    if success:
        return {"status": "registered"}

    return {"status": "user_exists"}


def login(email, password):

    user = get_user(email)

    if not user:
        return {"status": "no_user"}

    if user[2] != password:
        return {"status": "wrong_password"}

    return {
        "status": "login_success",
        "credits": user[3]
    }
