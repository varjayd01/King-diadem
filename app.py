from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

# พยายามเชื่อมสมองเดิม ถ้าพังให้ระบบยังลุกได้
try:
    from consciousness import consciousness
except Exception:
    consciousness = None

def _reply(text: str):
    text = text or ""
    if consciousness is None:
        return f"รับแล้ว: {text}"
    try:
        result = consciousness(text)
        if isinstance(result, dict):
            return (
                result.get("reply")
                or result.get("text")
                or result.get("data")
                or str(result)
            )
        return str(result)
    except Exception as e:
        return f"Backend error: {e}"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(req: Request):
    data = await req.json()
    msg = data.get("message", "")
    return JSONResponse({"reply": _reply(msg)})

# รองรับทั้ง 2 ชื่อ เผื่อหน้าเว็บเก่าของพี่เรียกคนละทาง
@app.post("/api/think")
async def api_think(req: Request):
    data = await req.json()
    msg = data.get("message", "")
    return JSONResponse({"reply": _reply(msg)})
