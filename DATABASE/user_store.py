import threading

users = {}

lock = threading.Lock()


def create_user(api_key):

    with lock:

        users[api_key] = {
            "plan": "free",
            "queries_today": 0
        }


def get_plan(api_key):

    with lock:

        if api_key not in users:
            return "free"

        return users[api_key]["plan"]


def set_plan(api_key, plan):

    with lock:

        if api_key not in users:
            users[api_key] = {}

        users[api_key]["plan"] = plan


def get_queries_today(api_key):

    with lock:

        if api_key not in users:
            return 0

        return users[api_key]["queries_today"]


def add_query(api_key):

    with lock:

        if api_key not in users:
            users[api_key] = {
                "plan": "free",
                "queries_today": 0
            }

        users[api_key]["queries_today"] += 1
