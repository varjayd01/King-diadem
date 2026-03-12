import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

# KING DIADEM CORE
from king_diadem_core import king_diadem

app = FastAPI(
    title="KING DIADEM",
    description="Civilization Decision Infrastructure",
    version="1.0"
)


# -----------------------------
# Request Model
# -----------------------------

class QuestionRequest(BaseModel):
    question: str


# -----------------------------
# Health Check
# -----------------------------

@app.get("/")
def root():
    return {
        "system": "KING DIADEM",
        "status": "running",
        "mode": "civilization decision engine"
    }


# -----------------------------
# Decision Endpoint
# -----------------------------

@app.post("/decision")
def decision(request: QuestionRequest):

    result = king_diadem(request.question)

    return result


# -----------------------------
# Emergency Mode
# -----------------------------

@app.post("/emergency")
def emergency(request: QuestionRequest):

    result = king_diadem(request.question)

    result["mode"] = "emergency"

    return result


# -----------------------------
# Server Launch
# -----------------------------

if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
