import os
import stripe
from fastapi import FastAPI, Request, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from core.truth_system import run_truth_infrastructure

app = FastAPI(title="KING DIADEM™ DriftZero OS")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# เชื่อมต่อ UI
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# ระบบจ่ายเงิน (Environment Variables)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@app.get("/")
def home():
    return FileResponse(os.path.join(BASE_DIR, "static", "index.html"))

@app.post("/ENGINE")
async def engine_endpoint(req: Request):
    data = await req.json()
    # ดันข้อมูลเข้าสู่โครงสร้างพื้นฐานสัจธรรม (รวม AI 3 ตัว + Survivor Engine)
    result = await run_truth_infrastructure(data["input"], data["state"])
    return result

@app.post("/api/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    # ระบบเฝ้าระวังท่อน้ำเลี้ยง (Credits)
    return {"status": "success"}
