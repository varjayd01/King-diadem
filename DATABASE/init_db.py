from DATABASE.db import get_conn

def init_db():

    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        api_key TEXT PRIMARY KEY,
        credits INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()
