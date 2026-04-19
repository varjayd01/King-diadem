# app.py

import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# 👉 ใช้ของพี่ ไม่เปลี่ยนชื่อ
from ENGINE.universal_engine import run_universal_engine

app = FastAPI(title="KING DIADEM")

# 📁 path static
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# 📦 input model
class InputData(BaseModel):
    input: str
    entropy: float = 40
    resource: float = 50
    stability: float = 60


# 🌐 หน้าเว็บหลัก
@app.get("/")
def home():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


# 🔥 ENGINE endpoint (จุดเดียวจบ)
@app.post("/ENGINE")
async def engine_endpoint(data: InputData):
    try:
        payload = data.dict()

        result = run_universal_engine(payload)

        # 👉 กันพัง ถ้า engine คืนค่า None
        if result is None:
            return {
                "status": "error",
                "message": "ENGINE returned None"
            }

        return result

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# 🚀 run local
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
