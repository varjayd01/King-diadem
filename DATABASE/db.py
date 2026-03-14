import sqlite3

DB_NAME = "king_diadem.db"

def get_conn():
    return sqlite3.connect(DB_NAME)
