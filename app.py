from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 🔥 CORS (จำเป็น)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "alive"}

@app.post("/chat")
async def chat(req: Request):
    data = await req.json()
    msg = data.get("message", "")

    return {
        "reply": f"รับแล้ว: {msg}"
    }
