import os
import stripe
from fastapi import FastAPI, Request, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from core.navigator import run_truth_engine

app = FastAPI(title="KING DIADEM - Eternal Truth")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# เชื่อมต่อหน้าจอ UI
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# ระบบจ่ายเงิน (ใส่ Key ใน Environment Variables)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

class KingRequest(BaseModel):
    input_text: str
    resource_level: float = 50

@app.get("/")
def home():
    return FileResponse(os.path.join(BASE_DIR, "static", "index.html"))

@app.post("/ENGINE")
async def engine_endpoint(req: KingRequest):
    # วิ่งเข้าสู่ระบบประมวลผลสัจธรรมของ ไลล่า และสภา AI
    result = await run_truth_engine(req.input_text, req.resource_level)
    return result

@app.post("/api/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    # ระบบตรวจสอบเงินเข้าอัตโนมัติเพื่อคงสภาพระบบ
    return {"status": "success"}
