from fastapi import APIRouter
from pydantic import BaseModel
import sqlite3

router = APIRouter()

class Register(BaseModel):
    email:str
    password:str

class Login(BaseModel):
    email:str
    password:str


@router.post("/register")
def register(user:Register):

    conn = sqlite3.connect("king_diadem.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users(email,password) VALUES (?,?)",
        (user.email,user.password)
    )

    conn.commit()

    return {"status":"user_created"}



@router.post("/login")
def login(user:Login):

    conn = sqlite3.connect("king_diadem.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (user.email,user.password)
    )

    result = cursor.fetchone()

    if result:
        return {"status":"login_success"}
    else:
        return {"status":"login_failed"}
