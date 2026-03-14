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
