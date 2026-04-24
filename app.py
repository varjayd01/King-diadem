from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# =========================
# 🔥 FIX ROOT (กันหน้าขาว 100%)
# =========================
@app.get("/")
def root():
    return FileResponse("static/index.html")

# static (ไฟล์อื่น เช่น css/js/image)
app.mount("/static", StaticFiles(directory="static"), name="static")

# =========================
# 🧠 ENGINE
# =========================
try:
    from ENGINE.decision_engine import DecisionEngine
    engine = DecisionEngine()
except Exception as e:
    print("ENGINE LOAD ERROR:", e)
    engine = None

@app.post("/run")
async def run_engine(data: dict):
    if engine:
        try:
            return engine.run(data)
        except Exception as e:
            return {"error": str(e)}
    return {"error": "ENGINE NOT FOUND"}

# =========================
# 🤖 AI
# =========================
@app.post("/ai")
async def ai_call(data: dict):
    try:
        from openai import OpenAI

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        prompt = data.get("input", "")

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return {"ai": res.choices[0].message.content}

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
# ❤️ HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return {"status": "alive 👑"}
