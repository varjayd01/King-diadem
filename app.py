from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from ENGINE.universal_engine import UNIVERSAL_ENGINE

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# ===== MEMORY (ไม่พัง) =====
users = {}
usage = {}
FREE_LIMIT = 50


# ===== ROOT =====
@app.get("/")
def root():
    return FileResponse("static/index.html")


# ===== REGISTER =====
@app.post("/register")
async def register(request: Request):
    form = await request.form()
    username = form.get("username")
    password = form.get("password")

    if not username or not password:
        return {"error": "missing"}

    if username in users:
        return {"error": "exists"}

    users[username] = password
    return {"status": "ok"}


# ===== LOGIN =====
@app.post("/login")
async def login(request: Request):
    form = await request.form()
    username = form.get("username")
    password = form.get("password")

    if users.get(username) != password:
        return {"error": "invalid"}

    return {"status": "ok"}


# ===== ENGINE INPUT =====
class Input(BaseModel):
    username: str
    location: str = ""
    food: str = ""
    money: str = ""
    risk: str = ""


# ===== ENGINE =====
@app.post("/ENGINE")
def run_engine(data: Input):

    if data.username not in users:
        return {"error": "no user"}

    usage.setdefault(data.username, 0)

    if usage[data.username] >= FREE_LIMIT:
        return {"error": "limit"}

    usage[data.username] += 1

    result = UNIVERSAL_ENGINE(data.dict())

    return result
