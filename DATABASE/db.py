import sqlite3, os

DB_PATH = os.getenv("DB_PATH", "data/king_diadem.db")

def get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS credits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            amount INTEGER DEFAULT 0,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS decision_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            input TEXT,
            route TEXT,
            response TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            amount_usd REAL,
            stripe_session_id TEXT,
            status TEXT DEFAULT 'pending',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

def log_decision(user_email, input_text, route, response):
    conn = get_conn()
    conn.execute("INSERT INTO decision_log (user_email,input,route,response) VALUES (?,?,?,?)",
                 (user_email, input_text, route, response))
    conn.commit()
    conn.close()

def get_credits(user_email):
    conn = get_conn()
    row = conn.execute("SELECT amount FROM credits WHERE user_email=? ORDER BY updated_at DESC LIMIT 1",
                       (user_email,)).fetchone()
    conn.close()
    return row["amount"] if row else 0

def add_credits(user_email, amount):
    conn = get_conn()
    conn.execute("INSERT INTO credits (user_email,amount) VALUES (?,?)", (user_email, amount))
    conn.commit()
    conn.close()

def record_payment(user_email, amount_usd, session_id):
    conn = get_conn()
    conn.execute("INSERT INTO payments (user_email,amount_usd,stripe_session_id,status) VALUES (?,?,?,'completed')",
                 (user_email, amount_usd, session_id))
    conn.commit()
    conn.close()
