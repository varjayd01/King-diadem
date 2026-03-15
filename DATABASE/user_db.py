import sqlite3

DB_NAME = "king_diadem.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT,
        credits INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


def create_user(email, password):

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    try:
        c.execute(
            "INSERT INTO users(email,password) VALUES(?,?)",
            (email, password)
        )
        conn.commit()
        return True
    except:
        return False

    finally:
        conn.close()


def get_user(email):

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    )

    user = c.fetchone()

    conn.close()

    return user


def add_credit(email, amount):

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        "UPDATE users SET credits = credits + ? WHERE email=?",
        (amount, email)
    )

    conn.commit()
    conn.close()
