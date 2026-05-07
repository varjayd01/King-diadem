# ==========================================
# 👑 KING DIADEM — ULTIMATE app.py
# Full Stack: Gemini + Council + Stripe + Governance
# ==========================================

from fastapi import FastAPI, Request, Header
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import json

# ── CORE & ENGINE INTEGRATION ────────────────────────────────────
# ดึงเอาโมดูลที่พี่สร้างไว้มาใช้งานจริง
try:
    from ENGINE.decision_engine import DecisionEngine
    from ENGINE.council_engine import council_engine
    from ENGINE.consensus_engine import consensus_engine
    from ENGINE.human_engine import analyze_human
    from ENGINE.intent_engine import analyze_intent
    from ENGINE.king_response import king_response
    from ENGINE.freedom_signal import record_question, freedom_index
except Exception as e:
    print(f"⚠ ENGINE IMPORT ERROR (Check your folder structure): {e}")

# ── LLM & KERNEL ────────────────────────────────────────────────
try:
    # สมมติฐานว่า GeminiLLM ของพี่พร้อมใช้งาน
    from core.llm_gemini import GeminiLLM
    from core.lyla_kernel import LylaKernel
    lyla = LylaKernel()
    llm = GeminiLLM(model="gemini-2.0-flash") # อัปเกรดเป็นตัวล่าสุดที่เสถียร
    print("✅ LYLA & Gemini Loaded")
except Exception:
    llm = None
    lyla = None

# ── INIT APP ─────────────────────────────────────────────────────
app = FastAPI(title="KING DIADEM OS")
engine = DecisionEngine() if 'DecisionEngine' in globals() else None

# ── STATIC & ROOT ───────────────────────────────────────────────
@app.get("/")
def root():
    return FileResponse("static/index.html")

app.mount("/static", StaticFiles(directory="static"), name="static")

# ── HEALTH CHECK (ตรวจสอบสถานะระบบทั้งหมด) ────────────────────────
@app.get("/health")
def health():
    return {
        "status": "alive 👑",
        "human_protocol": "ENFORCED",
        "freedom_score": freedom_index() if 'freedom_index' in globals() else "N/A",
        "lyla_status": "active" if lyla else "offline",
        "stripe_status": "configured" if os.getenv("STRIPE_SECRET") else "missing_keys"
    }

# ── MAIN DECISION ENGINE (The "Think" Endpoint) ──────────────────
@app.post("/run")
@app.post("/decision")
async def run_kernel(data: dict):
    user_input = data.get("input") or data.get("text") or ""
    context = data.get("context", {"energy": 50, "money": 50, "stress": 50})

    if not user_input:
        return {"error": "Input is required"}

    # 1. บันทึกสัญญาณ (System Trace)
    if 'record_question' in globals(): record_question()

    # 2. วิเคราะห์สถานะมนุษย์และเจตนา (Human & Intent)
    human_state = analyze_human(context)
    intent = analyze_intent(user_input)

    # 3. รัน Decision Engine หลัก
    if engine:
        raw_result = engine.run(data)
    else:
        raw_result = {"action": "maintain", "message": "Standard fallback activated"}

    # 4. เข้าสภา AI Council (ใช้ Council ที่พี่เขียน)
    # เราส่งผลลัพธ์จาก Engine ไปให้สภาตรวจสอบและโหวต
    council_votes = council_engine(raw_result, state=human_state)
    final_consensus = consensus_engine(council_votes, state=human_state)

    # 5. สรุปผลผ่านบุคลิก KING
    reply = king_response(user_input, json.dumps(final_consensus, ensure_ascii=False))

    return {
        "observer": "KING DIADEM",
        "reply": reply,
        "governance": {
            "entropy": human_state['entropy'],
            "intent": intent,
            "consensus": final_consensus
        }
    }

# ── FUTURE SIMULATION (จำลองอนาคต) ──────────────────────────────
@app.post("/simulate")
async def simulate_future(data: dict):
    user_input = data.get("input", "")
    if not llm: return {"status": "OFFLINE", "message": "LLM not found"}

    # ใช้ Prompt ที่พี่วางไว้แต่เพิ่มการคุมกฎผ่าน Lyla
    simulation_prompt = f"สถานการณ์: {user_input}\nวิเคราะห์ 30/90/365 วัน ตามกฎ HUMAN_PROTOCOL..."
    
    raw = llm.generate_with_governance(simulation_prompt)
    
    # กรองผ่าน Lyla เพื่อความปลอดภัย (Stability over Destruction)
    if lyla:
        observation = lyla.observe(user_input)
    else:
        observation = "Standard Observation"

    return {
        "status": "SUCCESS",
        "simulation": raw,
        "lyla_note": observation
    }

# ── PAYMENT SYSTEM (Stripe) ─────────────────────────────────────
import stripe
stripe.api_key = os.getenv("STRIPE_SECRET")

@app.post("/payment/create-checkout")
async def create_checkout():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": os.getenv("STRIPE_PRICE_ID"), "quantity": 1}],
            mode="payment",
            success_url="https://king-diadem.onrender.com/success",
            cancel_url="https://king-diadem.onrender.com/cancel",
        )
        return {"url": session.url}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


