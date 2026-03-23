from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import google.generativeai as genai

app = FastAPI()

# ===== CONFIG =====
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

# ===== STATIC =====
app.mount("/static", StaticFiles(directory="static"), name="static")

# ===== ROUTE =====
@app.get("/", response_class=HTMLResponse)
async def index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

# ===== HEALTH =====
@app.get("/system/health")
async def health():
    return {"status": "OK", "engine": "KING DIADEM"}

# ===== DECISION ENGINE =====
@app.post("/decision")
async def decision(request: Request):
    data = await request.json()
    user_input = data.get("input", "")

    # 🔥 safety layer
    if "ฆ่า" in user_input:
        return {"result": "ระบบไม่สนับสนุนความรุนแรง"}

    # 🔥 Gemini
    response = model.generate_content(user_input)
    reply = response.text

    return {"result": f"KING DIADEM:\n{reply}"}
