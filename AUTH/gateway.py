from AUTH.auth_system import authorize
from AUTH.api_key_manager import use_credit

def gateway(username: str):
    # 🔐 ตรวจ auth
    auth = authorize(username)

    if auth["status"] != "allowed":
        return {
            "status": "blocked",
            "reason": "no credits"
        }

    # 💸 ตัดเครดิต
    ok = use_credit(username, 1)

    if not ok:
        return {
            "status": "blocked",
            "reason": "credit exhausted"
        }

    return {
        "status": "ok"
    }
