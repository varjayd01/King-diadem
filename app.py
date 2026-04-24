from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# =========================
# 🔥 FIX ROOT (กันหน้าขาว)
# =========================
@app.get("/")
def root():
    return FileResponse("static/index.html")

app.mount("/static", StaticFiles(directory="static"), name="static")

# =========================
# 🧠 ENGINE (Observer)
# =========================
try:
    from ENGINE.decision_engine import DecisionEngine
    engine = DecisionEngine()
except Exception as e:
    print("ENGINE LOAD ERROR:", e)
    engine = None

# =========================
# ⚡ ENERGY GOVERNOR
# =========================
try:
    from ENGINE.energy_governor import allow_request
except:
    def allow_request(x):
        return True, {"energy": "unknown"}

# =========================
# 🧠 RUN ENGINE
# =========================
@app.post("/run")
async def run_engine(data: dict):

    if not engine:
        return {"error": "ENGINE NOT FOUND"}

    try:
        return engine.run(data)
    except Exception as e:
        return {"error": str(e)}

# =========================
# 🤖 AI (CONNECTED VERSION)
# =========================
@app.post("/ai")
async def ai_call(data: dict):

    api_key = "public"  # อนาคตเปลี่ยนเป็น user id

    ok, info = allow_request(api_key)

    if not ok:
        return {"ai": f"BLOCKED: {info}"}

    try:
        from openai import OpenAI

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # 👁️ ใช้ Decision ก่อน
        decision_result = None
        if engine:
            try:
                decision_result = engine.run(data)
            except Exception as e:
                decision_result = {"error": str(e)}

        prompt = f"""
SYSTEM (Decision Observer):
{decision_result}

USER:
{data.get("input", "")}
"""

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "ai": res.choices[0].message.content,
            "decision": decision_result,
            "energy": info
        }

    except Exception as e:
        return {"ai": f"[AI ERROR] {str(e)}"}

# =========================
# 💳 STRIPE
# =========================
import stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@app.post("/create-checkout-session")
def create_checkout():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price": os.getenv("STRIPE_PRICE_ID"),
                "quantity": 1,
            }],
            mode="payment",
            success_url="https://king-diadem.onrender.com/",
            cancel_url="https://king-diadem.onrender.com/",
        )

        return {"url": session.url}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# =========================
# ❤️ HEALTH
# =========================
@app.get("/health")
def health():
    return {"status": "alive 👑"}
