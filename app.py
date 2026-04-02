from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/", StaticFiles(directory="static", html=True), name="static")

class Input(BaseModel):
    input: str

@app.post("/decision")
def decision(data: Input):
    text = data.input

    risk = 0
    tier = "T2"

    if "โกง" in text or "ผิด" in text:
        risk += 2

    if "ฆ่า" in text or "ทำร้าย" in text:
        risk += 5

    if risk >= 5:
        return {
            "response": "⛔ STOP THE LINE",
            "tier": "K12",
            "risk": risk
        }

    return {
        "response": "✅ ผ่าน",
        "tier": tier,
        "risk": risk
    }
