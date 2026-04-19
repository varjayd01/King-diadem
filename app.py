import os
import time
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from ENGINE.universal_engine import run_universal_engine

app = FastAPI(title="KING DIADEM")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# =========================
# 📦 USER STORAGE (ชั่วคราว)
# =========================
USER_DB = {
    "demo": {
        "plan": "FREE",
        "credits": 5,
        "last_reset": time.time()
    }
}

RESET_INTERVAL = 86400  # 24 ชม


# =========================
# 🧠 PACKAGE CHECK
# =========================
def check_and_consume(user_id: str):
    user = USER_DB.get(user_id)

    if not user:
        return False, "NO_USER", None

    # รีเซ็ตเครดิตทุกวัน
    if time.time() - user["last_reset"] > RESET_INTERVAL:
        user["credits"] = 5 if user["plan"] == "FREE" else 999
        user["last_reset"] = time.time()

    if user["credits"] <= 0:
        return False, "NO_CREDIT", user

    user["credits"] -= 1
    return True, "OK", user


# =========================
# 📥 INPUT MODEL
# =========================
class InputData(BaseModel):
    input: str
    entropy: float = 40
    resource: float = 50
    stability: float = 60


# =========================
# 🌐 FRONTEND
# =========================
@app.get("/")
def home():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


# =========================
# 🔥 ENGINE GATE
# =========================
@app.post("/ENGINE")
async def engine_endpoint(data: InputData, request: Request):

    # 🧠 ดึง user (ตอนนี้ mock ก่อน)
    user_id = "demo"

    ok, status, user = check_and_consume(user_id)

    if not ok:
        return {
            "status": "blocked",
            "reason": status,
            "credits": user["credits"] if user else 0,
            "plan": user["plan"] if user else "NONE"
        }

    try:
        result = run_universal_engine(data.dict())

        return {
            "status": "ok",
            "plan": user["plan"],
            "credits": user["credits"],
            "data": result
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# =========================
# 🚀 RUN
# =========================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
