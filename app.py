import os
import stripe
from fastapi import FastAPI, Request, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# 🔒 SAFE IMPORT
try:
    from core.truth_system import run_truth_infrastructure
except Exception as e:
    run_truth_infrastructure = None
    print("IMPORT ERROR:", e)

app = FastAPI(title="KING DIADEM™ DriftZero OS")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 🔒 STATIC SAFE
static_path = os.path.join(BASE_DIR, "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

# 🔒 STRIPE SAFE
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# 🧪 HEALTH CHECK
@app.get("/alive")
def alive():
    return {"status": "king is alive"}

# 🏠 HOME
@app.get("/")
def home():
    index_path = os.path.join(static_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "index.html not found"}

# ⚙️ ENGINE
@app.post("/ENGINE")
async def engine_endpoint(req: Request):
    data = await req.json()

    if run_truth_infrastructure is None:
        return {"error": "engine not ready"}

    result = await run_truth_infrastructure(
        data.get("input"),
        data.get("state")
    )
    return result

# 💳 STRIPE WEBHOOK
@app.post("/api/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    return {"status": "success"}
