from DATABASE.db import get_conn

def get_credits(api_key):

    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT credits FROM users WHERE api_key=?", (api_key,))
    row = c.fetchone()

    conn.close()

    if not row:
        return 0

    return row[0]


def add_credits(api_key, amount):

    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    INSERT INTO users(api_key,credits)
    VALUES(?,?)
    ON CONFLICT(api_key)
    DO UPDATE SET credits=credits+?
    """,(api_key,amount,amount))

    conn.commit()
    conn.close()


def use_credit(api_key):

    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT credits FROM users WHERE api_key=?", (api_key,))
    row = c.fetchone()

    if not row or row[0] <= 0:
        conn.close()
        return False

    c.execute(
        "UPDATE users SET credits=credits-1 WHERE api_key=?",
        (api_key,)
    )

    conn.commit()
    conn.close()

    return True
