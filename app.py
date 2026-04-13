from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

import os
import requests

# ===== IMPORT FATE =====
from core.fate_core import run_fate

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return FileResponse("static/index.html")


# ===== ENV =====
OPENAI_API_KEY = os.getenv("CHATGPT_API_KEY")


# ===== INPUT =====
class ChatInput(BaseModel):
    message: str


# ===== AI CALL =====
def call_openai(message):

    url = "https://api.openai.com/v1/responses"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4.1-mini",
        "input": message
    }

    try:
        r = requests.post(url, headers=headers, json=data)
        res = r.json()
        return res["output"][0]["content"][0]["text"]
    except:
        return "ระบบตอบไม่ได้ชั่วคราว"


# ===== HUMAN-AWARE LAYER =====
def human_layer(message, ai_reply, risk):

    # ไม่ใช่อารมณ์ แต่เป็น “การกันพัง”
    if risk == "normal":
        return ai_reply

    if risk == "low":
        return f"(ข้อมูลยังไม่ชัด) {ai_reply}"

    return ai_reply


# ===== CHAT =====
@app.post("/chat")
def chat(data: ChatInput):

    # ===== FATE =====
    fate = run_fate(data.dict())

    if fate["status"] == "reject":
        return {"reply": "[FATE REJECTED] invalid input"}

    if fate["status"] == "block":
        return {"reply": fate["safe_response"]}

    clean = fate["data"]
    risk = fate["risk"]

    # ===== AI =====
    ai_reply = call_openai(clean["message"])

    # ===== HUMAN LAYER =====
    final = human_layer(clean["message"], ai_reply, risk)

    return {
        "reply": final,
        "risk": risk
    }
