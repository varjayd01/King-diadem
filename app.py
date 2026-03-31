from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# mount static
app.mount("/static", StaticFiles(directory="static"), name="static")

# serve หน้าเว็บ
@app.get("/")
def root():
    return FileResponse("static/index.html")

# schema
class Input(BaseModel):
    message: str

# decision endpoint
@app.post("/decision")
def decision(data: Input):
    return {
        "reply": f"KING DIADEM: {data.message}"
    }
