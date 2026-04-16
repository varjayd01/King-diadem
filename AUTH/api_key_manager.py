import sqlite3

DB = "king_diadem.db"


def use_credit(username: str, amount: int = 1):

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT credits FROM users WHERE username=?",
        (username,)
    )

    result = cursor.fetchone()

    if not result:
        return False

    credits = result[0]

    if credits < amount:
        return False

    cursor.execute(
        "UPDATE users SET credits = credits - ? WHERE username=?",
        (amount, username)
    )

    conn.commit()
    conn.close()

    return True
