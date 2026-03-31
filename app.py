from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# serve static
app.mount("/static", StaticFiles(directory="static"), name="static")

# หน้าเว็บหลัก
@app.get("/")
def root():
    return FileResponse("static/index.html")

# schema
class Input(BaseModel):
    message: str

# API
@app.post("/decision")
def decision(data: Input):
    msg = data.message

    # logic ง่ายๆ (พัฒนาเพิ่มได้)
    if "เสี่ยง" in msg:
        reply = "⚠️ Risk detected"
    elif "ทางเลือก" in msg:
        reply = "คุณยังมีอย่างน้อย 1 ทางเสมอ"
    else:
        reply = f"KING DIADEM: {msg}"

    return {"reply": reply}
