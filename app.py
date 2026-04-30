# app.py
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

# =========================
# IMPORT KING DIADEM CORE
# =========================
try:
    from core.llm_gemini import GeminiLLM
    from ENGINE.decision_engine import DecisionEngine
except Exception as e:
    print(f"IMPORT ERROR: {e}")
    GeminiLLM = None
    DecisionEngine = None

app = FastAPI(title="King-Diadem Decision Engine")

# =========================
# STATIC FILES
# =========================
@app.get("/")
def root():
    return FileResponse("static/index.html")

app.mount("/static", StaticFiles(directory="static"), name="static")

# =========================
# INITIALIZE ENGINES
# =========================
llm = None
engine = None

try:
    if GeminiLLM:
        llm = GeminiLLM(model="gemini-2.5-flash")
    
    if DecisionEngine:
        engine = DecisionEngine()          # จะเรียก __init__ ของ DecisionEngine
    
    print("✅ King-Diadem initialized successfully")
except Exception as e:
    print(f"❌ ENGINE INITIALIZATION FAILED: {e}")
    engine = None

# =========================
# MAIN ENDPOINT
# =========================
@app.post("/run")
@app.post("/decision")   # รองรับทั้งสอง path
async def run_engine(data: dict):
    user_input = data.get("input") or data.get("text") or data.get("message") or ""

    if not user_input:
        return {
            "observer": "KING DIADEM",
            "status": "ERROR",
            "message": "ไม่พบ input ใน request"
        }

    # ถ้า engine โหลดไม่สำเร็จ ให้ fallback
    if not engine:
        return {
            "observer": "KING DIADEM",
            "status": "ENGINE OFFLINE",
            "fallback": [
                "ลดการใช้ทรัพยากร",
                "หาความร่วมมือ",
                "รักษาความปลอดภัย",
                "ย้ายไปพื้นที่เสี่ยงต่ำ"
            ]
        }

    payload = {"input": user_input}

    try:
        result = engine.run(payload)
        return result

    except Exception as e:
        print(f"Run Engine Error: {e}")
        return {
            "observer": "KING DIADEM",
            "status": "ERROR",
            "error": str(e),
            "fallback": [
                "รักษาสถานการณ์ปัจจุบัน",
                "ลดความเสี่ยงทันที",
                "ขอความช่วยเหลือจากภายนอก",
                "หลีกเลี่ยงการตัดสินใจใหญ่"
            ]
        }


# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health():
    status = {
        "status": "alive 👑",
        "engine_loaded": engine is not None,
        "llm_loaded": llm is not None,
        "model": getattr(llm, "model", None) if llm else None
    }
    return status


# =========================
# OPTIONAL: แสดงข้อมูลระบบ
# =========================
@app.get("/status")
def system_status():
    return {
        "service": "King-Diadem",
        "version": "0.1.0",
        "llm": "Gemini" if llm else "None",
        "engine": "Loaded" if engine else "Offline",
        "message": "DriftZero Governance Framework"
    }
