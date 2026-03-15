import os
import uvicorn

from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from ENGINE.decision_engine import run_decision
from DATABASE.credit_store import use_credit, get_credits
from AUTH.api_keys import create_api_key

app = FastAPI(
    title="KING DIADEM",
    version="0.5",
    description="Reality Optimization Decision Engine"
)

# =========================
# STATIC FILES
# =========================

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# =========================
# HOME
# =========================

@app.get("/", response_class=HTMLResponse)
async def home():

    path = "INTERFACE/dashboard.html"

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    return "<h1>KING DIADEM</h1>"

# =========================
# CREATE API KEY
# =========================

@app.get("/auth/create-key")
async def create_key():

    key = create_api_key()

    return {
        "api_key": key,
        "credits": get_credits(key)
    }

# =========================
# SYSTEM STATUS
# =========================

@app.get("/system")
async def system():

    return {
        "status": "running",
        "engine": "online",
        "credits": "active"
    }

# =========================
# DECISION ENGINE
# =========================

@app.post("/decision")
async def decision(
    request: Request,
    api_key: str = Header(...)
):

    # ป้องกัน body ว่าง
    try:
        body = await request.json()
    except:
        body = {}

    credits = get_credits(api_key)

    if credits <= 0:
        raise HTTPException(
            status_code=402,
            detail="No credits"
        )

    success = use_credit(api_key)

    if not success:
        raise HTTPException(
            status_code=400,
            detail="Credit error"
        )

    try:
        result = run_decision(body)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Decision engine error: {str(e)}"
        )

    return {
        "decision": result,
        "credits_left": get_credits(api_key)
    }

# =========================
# HEALTH CHECK
# =========================

@app.get("/health")
async def health():

    return {
        "status": "ok"
    }

# =========================
# SERVER START
# =========================

if __name__ == "__main__":

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=10000
    )
