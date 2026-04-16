from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import BaseModel

import os
import requests
import stripe

from core.fate_core import run_fate
from KING_DIAdem_core import king_diadem

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")


# ===== ENV =====
OPENAI_API_KEY = os.getenv("CHATGPT_API_KEY")
stripe.api_key = os.getenv("STRIPE_SECRET")


# ===== INPUT =====
class ChatInput(BaseModel):
    message: str

class EngineInput(BaseModel):
    username: str
    location: str
    food: str
    money: str
    risk: str


# ===== CHAT =====
@app.post("/chat")
def chat(data: ChatInput):
    fate = run_fate(data.dict())

    if fate["status"] == "reject":
        return {"reply": "invalid"}

    clean = fate["data"]

    return {"reply": clean["message"]}


# ===== ENGINE =====
@app.post("/ENGINE")
def run_engine(data: EngineInput):

    question = f"""
    user: {data.username}
    location: {data.location}
    food: {data.food}
    money: {data.money}
    risk: {data.risk}
    """

    result = king_diadem(question)
    return result


# ===== STRIPE =====
@app.get("/pay")
def pay():

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price": os.getenv("STRIPE_PRICE_ID"),
            "quantity": 1,
        }],
        mode="payment",
        success_url="https://king-diadem.onrender.com/?success=1",
        cancel_url="https://king-diadem.onrender.com/?cancel=1",
    )

    return RedirectResponse(session.url)
