import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# 🔥 แก้ให้รองรับทั้ง ENGINE / engine
try:
    from ENGINE.core import run_engine
except:
    from engine.core import run_engine

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 🔥 fix path กัน Render มองไม่เจอ
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


@app.api_route("/", methods=["GET", "HEAD"])
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        text = data.get("message", "")
        reply = run_engine(text)
        return JSONResponse({"reply": reply})
    except Exception as e:
        return JSONResponse({"reply": f"ERROR: {str(e)}"})
