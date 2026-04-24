from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
import stripe
import os

app = FastAPI()

# =========================
# 🔐 CONFIG
# =========================
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# =========================
# ❤️ ROOT (แก้จอขาวตรงนี้)
# =========================
@app.get("/")
def root():
    return FileResponse("static/index.html")

# =========================
# 🧠 ENGINE
# =========================
try:
    from ENGINE.decision_engine import DecisionEngine
    engine = DecisionEngine()
except Exception as e:
    print("ENGINE LOAD FAIL:", e)
    engine = None

# =========================
# 🧠 RUN ENGINE
# =========================
@app.post("/run")
async def run_engine(data: dict):

    if engine:
        try:
            result = engine.run(data)
        except Exception as e:
            result = {"error": str(e)}
    else:
        result = {"error": "ENGINE NOT FOUND"}

    return result

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
# 💳 STRIPE CHECKOUT
# =========================
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
            success_url="https://king-diadem.onrender.com/success",
            cancel_url="https://king-diadem.onrender.com/cancel",
        )

        return {"url": session.url}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# =========================
# 🔔 STRIPE WEBHOOK
# =========================
@app.post("/webhook")
async def stripe_webhook(request: Request):

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            os.getenv("STRIPE_WEBHOOK_SECRET")
        )

        if event["type"] == "checkout.session.completed":
            print("✅ PAYMENT SUCCESS")

        return {"status": "ok"}

    except Exception as e:
        return {"error": str(e)}

# =========================
# 🧪 HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return {"status": "alive 👑"}
