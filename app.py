from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.templating import Jinja2Templates

from engine.brain import think
from engine.memory import reset_state

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI(title="King Diadem", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_name": "King Diadem",
        },
    )


@app.get("/health")
async def health():
    return {"status": "alive"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)


@app.post("/api/think")
async def api_think(req: Request):
    data = await req.json()
    message = data.get("message", "")
    mode = data.get("mode", "chat")
    session_id = data.get("session_id", "default")
    seed = data.get("seed", "")

    result = think(
        message=message,
        mode=mode,
        session_id=session_id,
        seed=seed,
    )
    return JSONResponse(result)


@app.post("/api/reset")
async def api_reset(req: Request):
    data = await req.json()
    session_id = data.get("session_id", "default")
    reset_state(session_id)
    return JSONResponse({"ok": True, "session_id": session_id})


@app.post("/chat")
async def chat(req: Request):
    data = await req.json()
    message = data.get("message", "")
    result = think(
        message=message,
        mode="chat",
        session_id="legacy",
        seed="",
    )
    return JSONResponse({"reply": result["reply"]})
