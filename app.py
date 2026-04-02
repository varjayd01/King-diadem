from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 🔥 serve frontend จาก backend เลย (จบปัญหา Pages)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# 🔥 CORS กันยิงพัง
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
