import os
import uvicorn

from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from ENGINE.decision_engine import run_decision

from DATABASE.credit_store import use_credit, get_credits
from DATABASE.user_store import get_plan, get_queries_today, add_query, set_plan

from GLOBAL_NODE.feed_store import add_feed_entry, get_feed

from AUTH.api_keys import create_api_key


app = FastAPI(
    title="KING DIADEM",
    version="0.7",
    description="Reality Optimization Decision Engine"
)

# =========================
# STATIC
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
        "api_key": key
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

    try:
        body = await request.json()
    except:
        body = {}

    plan = get_plan(api_key)

    # -------------------------
    # FREE PLAN LIMIT
    # -------------------------

    if plan == "free":

        queries = get_queries_today(api_key)

        if queries >= 5:

            raise HTTPException(
                status_code=403,
                detail="Free plan limit reached. Upgrade to PRO."
            )

        add_query(api_key)

    # -------------------------
    # CREDIT CHECK
    # -------------------------

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

    # -------------------------
    # RUN DECISION ENGINE
    # -------------------------

    try:

        result = run_decision(body)

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Decision engine error: {str(e)}"
        )

    # -------------------------
    # GLOBAL FEED
    # -------------------------

    add_feed_entry(api_key, result)

    return {
        "decision": result,
        "plan": plan,
        "credits_left": get_credits(api_key)
    }


# =========================
# GLOBAL DECISION FEED
# =========================

@app.get("/global-feed")
async def global_feed():

    data = get_feed()

    return {
        "decisions": data
    }


# =========================
# UPGRADE PLAN (TEST)
# =========================

@app.get("/upgrade/pro")
async def upgrade_pro(api_key: str = Header(...)):

    set_plan(api_key, "pro")

    return {
        "status": "upgraded",
        "plan": "pro"
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
