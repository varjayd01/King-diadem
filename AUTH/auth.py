from fastapi import APIRouter
from pydantic import BaseModel
import sqlite3

router = APIRouter()

DB = "king_diadem.db"

# ===== INIT DB =====
def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        credits INTEGER DEFAULT 0,
        paid INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()

init_db()


# ===== MODELS =====
class Register(BaseModel):
    username: str
    password: str

class Login(BaseModel):
    username: str
    password: str


# ===== REGISTER =====
@router.post("/register")
def register(user: Register):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users(username,password) VALUES (?,?)",
            (user.username, user.password)
        )
        conn.commit()
        return {"status": "created"}

    except:
        return {"status": "exists"}

    finally:
        conn.close()


# ===== LOGIN =====
@router.post("/login")
def login(user: Login):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password,credits,paid FROM users WHERE username=?",
        (user.username,)
    )

    result = cursor.fetchone()
    conn.close()

    if not result:
        return {"status": "no_user"}

    if result[0] != user.password:
        return {"status": "wrong"}

    return {
        "status": "ok",
        "credits": result[1],
        "paid": result[2]
    }


# ===== ADD CREDIT =====
@router.post("/add_credit/{username}/{amount}")
def add_credit(username: str, amount: int):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET credits = credits + ? WHERE username=?",
        (amount, username)
    )

    conn.commit()
    conn.close()

    return {"status": "credited"}


# ===== SET PAID =====
@router.post("/set_paid/{username}")
def set_paid(username: str):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET paid = 1 WHERE username=?",
        (username,)
    )

    conn.commit()
    conn.close()

    return {"status": "paid"}
