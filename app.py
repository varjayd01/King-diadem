from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

from core.orchestrator import Orchestrator

app = Flask(__name__, static_folder="static")
CORS(app)

orch = Orchestrator()


# ===== FRONTEND =====
@app.route("/")
def home():
    return send_from_directory("static", "index.html")


# ===== CHAT =====
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json

    result = orch.run(
        user_input=data.get("message"),
        context=data
    )

    return jsonify(result)


# ===== HEALTH =====
@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(debug=True)
