# =========================
# 👑 KING DIADEM — app.py
# Full Stack: Gemini + LYLA + Stripe + Future Simulation
# =========================

from fastapi import FastAPI, Request, Header
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os

# ── CORE ──────────────────────────────────────────────────────────
try:
    from core.llm_gemini import GeminiLLM
    from core.emptiness_guard import emptiness_guard
    from core.core_loop import run_core
except Exception as e:
    print(f"CORE IMPORT ERROR: {e}")
    GeminiLLM = None
    emptiness_guard = None
    run_core = None

# ── LYLA KERNEL ───────────────────────────────────────────────────
try:
    from core.lyla_kernel import LylaKernel
    lyla = LylaKernel()
    print("✅ LYLA Kernel loaded")
except Exception as e:
    print(f"⚠ LYLA Kernel not loaded: {e}")
    lyla = None

# ── ENGINE ────────────────────────────────────────────────────────
try:
    from ENGINE.decision_engine import DecisionEngine
    from ENGINE.pattern_engine import analyze_pattern
except Exception as e:
    print(f"ENGINE IMPORT ERROR: {e}")
    DecisionEngine = None
    analyze_pattern = None

# ── PAYMENT ───────────────────────────────────────────────────────
try:
    import stripe
    stripe.api_key = os.getenv("STRIPE_SECRET")
    STRIPE_PRICE_ID = os.getenv("STRIPE_PRICE_")
    STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_")
    from DATABASE.user_db import add_credit, init_db
    init_db()
    STRIPE_OK = True
    print("✅ Stripe + DB loaded")
except Exception as e:
    print(f"⚠ Stripe/DB not loaded: {e}")
    STRIPE_OK = False

# ── INIT ──────────────────────────────────────────────────────────
app = FastAPI(title="King-Diadem Decision Engine")

llm = None
engine = None

try:
    if GeminiLLM:
        llm = GeminiLLM(model="gemini-2.5-flash")
    if DecisionEngine:
        engine = DecisionEngine()
    print("✅ King-Diadem initialized")
except Exception as e:
    print(f"❌ ENGINE INIT FAILED: {e}")

# ── STATIC ────────────────────────────────────────────────────────
@app.get("/")
def root():
    return FileResponse("static/index.html")

app.mount("/static", StaticFiles(directory="static"), name="static")

# ── HEALTH ────────────────────────────────────────────────────────
@app.get("/health")
def health():
    return {
        "status": "alive 👑",
        "engine_loaded": engine is not None,
        "llm_loaded": llm is not None,
        "lyla_loaded": lyla is not None,
        "stripe_loaded": STRIPE_OK,
        "model": getattr(llm, "model", None) if llm else None
    }

# ── MAIN DECISION ENGINE ──────────────────────────────────────────
@app.post("/run")
@app.post("/decision")
async def run_engine(data: dict):
    user_input = data.get("input") or data.get("text") or data.get("message") or ""

    if not user_input:
        return {"observer": "KING DIADEM", "status": "ERROR", "message": "ไม่พบ input"}

    # fallback ถ้า engine offline
    if not engine:
        return {
            "observer": "KING DIADEM",
            "status": "ENGINE OFFLINE",
            "fallback": ["ลดการใช้ทรัพยากร", "หาความร่วมมือ", "รักษาความปลอดภัย", "ย้ายไปพื้นที่เสี่ยงต่ำ"]
        }

    try:
        result = engine.run(data)
        return result
    except Exception as e:
        return {"observer": "KING DIADEM", "status": "ERROR", "error": str(e)}


# ── FUTURE SIMULATION (จำลองอนาคตหลายเส้นทาง) ───────────────────
@app.post("/simulate")
async def simulate_future(data: dict):
    """
    รับ: input (สถานการณ์), paths (list ของทางเลือก)
    คืน: แต่ละทางเลือกจะเจออะไรถ้าเดินไปเรื่อยๆ
    """
    user_input = data.get("input", "")
    paths = data.get("paths", [])

    if not user_input:
        return {"status": "ERROR", "message": "ไม่พบ input"}

    if not llm:
        return {"status": "ENGINE OFFLINE", "message": "Gemini ไม่พร้อม"}

    # ถ้าไม่ส่ง paths มา ให้ระบบสร้างเองจาก pattern
    if not paths:
        paths = ["เดินหน้าต่อแบบเดิม", "หยุดและประเมินใหม่", "หาพันธมิตร/ทรัพยากรเพิ่ม", "ถอยและ pivot"]

    simulation_prompt = f"""สถานการณ์: {user_input}

จำลองอนาคตสำหรับแต่ละทางเลือกต่อไปนี้ โดยวิเคราะห์แบบกลางๆ ไม่ตัดสิน ไม่ว่าจะเป็นสีขาว เทา หรือดำ:

{chr(10).join([f'{i+1}. {p}' for i, p in enumerate(paths)])}

สำหรับแต่ละทางเลือก ให้ระบุ:
- ผลลัพธ์ที่น่าจะเกิดใน 30 วัน / 90 วัน / 1 ปี
- จุดที่ระบบจะเริ่ม "พัง" (Collapse Signal)
- ทางเลือกที่เหลืออยู่ (Remaining Choice)
- คะแนน Drift Risk (0-100)

ตอบแบบตรงไปตรงมา ระบุความเสี่ยงจริง ไม่เน้น optimism เกินจริง"""

    try:
        raw = llm.generate_with_governance(simulation_prompt, additional_context=user_input)

        # ถ้ามี LYLA kernel ให้กรองผ่านด้วย
        lyla_note = None
        if lyla:
            try:
                lyla_note = lyla.observe(user_input)
            except Exception:
                pass

        return {
            "observer": "KING DIADEM",
            "status": "SUCCESS",
            "simulation": raw,
            "paths_analyzed": paths,
            "lyla_observation": lyla_note
        }

    except Exception as e:
        return {"status": "ERROR", "error": str(e)}


# ── STRIPE CHECKOUT ───────────────────────────────────────────────
@app.post("/payment/create-checkout")
async def payment_checkout():
    if not STRIPE_OK:
        return JSONResponse({"error": "Stripe ยังไม่พร้อม"}, status_code=503)
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": STRIPE_PRICE_ID, "quantity": 1}],
            mode="payment",
            success_url="https://king-diadem.onrender.com/success",
            cancel_url="https://king-diadem.onrender.com/cancel",
        )
        return {"url": session.url}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


# ── STRIPE WEBHOOK ────────────────────────────────────────────────
_processed_events = set()

@app.post("/payment/webhook")
async def payment_webhook(
    request: Request,
    stripe_signature: str = Header(None, alias="stripe-signature")
):
    payload = await request.body()
    try:
        event = stripe.Webhook.construct_event(payload, stripe_signature, STRIPE_WEBHOOK_SECRET)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)

    event_id = event["id"]
    if event_id in _processed_events:
        return JSONResponse({"status": "duplicate"})
    _processed_events.add(event_id)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        email = session.get("customer_details", {}).get("email", "")
        amount = session.get("amount_total", 0) // 100
        if email:
            try:
                add_credit(email, amount)
                print(f"✅ Credit added: {email} +{amount}")
            except Exception as e:
                print(f"❌ add_credit failed: {e}")

    return JSONResponse({"status": "ok"})


# ── SUCCESS / CANCEL ──────────────────────────────────────────────
@app.get("/success")
def success():
    return HTMLResponse("""
    <html><body style='background:#000;color:#00ff88;font-family:monospace;display:flex;align-items:center;justify-content:center;height:100vh;'>
    <div style='text-align:center'>
        <h1>✅ ชำระเงินสำเร็จ</h1>
        <p>เครดิตจะเข้าระบบภายในไม่กี่วินาที</p>
        <a href='/' style='color:#00ccff'>← กลับ King Diadem</a>
    </div></body></html>
    """)

@app.get("/cancel")
def cancel():
    return HTMLResponse("""
    <html><body style='background:#000;color:#ff5e5e;font-family:monospace;display:flex;align-items:center;justify-content:center;height:100vh;'>
    <div style='text-align:center'>
        <h1>❌ ยกเลิกการชำระเงิน</h1>
        <a href='/' style='color:#00ccff'>← กลับหน้าหลัก</a>
    </div></body></html>
    """)
