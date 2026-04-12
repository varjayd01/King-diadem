import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# ===== IMPORT APP =====
try:
    from app import app
except:
    # fallback กันพัง
    app = FastAPI()

    @app.get("/")
    def fallback():
        return {"status": "main fallback working"}


# ===== STATIC (กันพัง) =====
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    pass


# ===== ROOT FALLBACK =====
@app.get("/health")
def health():
    return {"status": "ok"}


# ===== RUN =====
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
