import secrets
import sqlite3

DB = "king_diadem.db"


def create_api_key(username: str):
    key = "kd_" + secrets.token_hex(16)

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET credits = credits + 100 WHERE username=?",
        (username,)
    )

    conn.commit()
    conn.close()

    return key
