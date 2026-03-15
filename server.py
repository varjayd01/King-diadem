from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from DATABASE.db import init_db
from AUTH.auth import router as auth_router
from PAYMENT.stripe_payment import create_checkout

app = FastAPI()

init_db()

app.include_router(auth_router)


@app.get("/")
def root():
    return {"system":"KING DIADEM ONLINE"}



@app.get("/health")
def health():
    return {"status":"ok"}



@app.post("/create-checkout")
def checkout():

    url = create_checkout()

    return {"checkout_url":url}
