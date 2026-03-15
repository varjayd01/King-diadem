import os
import uvicorn

from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from ENGINE.decision_engine import run_decision
from DATABASE.credit_store import use_credit, get_credits
from AUTH.api_keys import create_api_key, is_valid_key


app = FastAPI(title="KING DIADEM")


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

    return "<h1>KING DIADEM Decision OS</h1>"


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

        "domains": [
            "life",
            "business",
            "survival",
            "world"
        ]
    }


# =========================
# GENERIC DECISION API
# =========================

@app.post("/decision")
async def decision(
    request: Request,
    api_key: str = Header(...)
):

    if not is_valid_key(api_key):

        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

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

    result = run_decision(body)

    return {

        "result": result,
        "credits_left": get_credits(api_key)

    }


# =========================
# LIFE DOMAIN
# =========================

@app.post("/analyze-life")
async def analyze_life(
    request: Request,
    api_key: str = Header(...)
):

    body = await request.json()

    body["domain"] = "life"

    result = run_decision(body)

    return result


# =========================
# BUSINESS DOMAIN
# =========================

@app.post("/analyze-business")
async def analyze_business(
    request: Request,
    api_key: str = Header(...)
):

    body = await request.json()

    body["domain"] = "business"

    result = run_decision(body)

    return result


# =========================
# SURVIVAL DOMAIN
# =========================

@app.post("/analyze-survival")
async def analyze_survival(
    request: Request,
    api_key: str = Header(...)
):

    body = await request.json()

    body["domain"] = "survival"

    result = run_decision(body)

    return result


# =========================
# WORLD DOMAIN
# =========================

@app.post("/analyze-world")
async def analyze_world(
    request: Request,
    api_key: str = Header(...)
):

    body = await request.json()

    body["domain"] = "world"

    result = run_decision(body)

    return result


# =========================
# SERVER START
# =========================

if __name__ == "__main__":

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=10000
    )
