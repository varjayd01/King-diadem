from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder="static")

# =========================
# ROOT (TEST SERVER)
# =========================
@app.route("/")
def home():
    return "KING DIADEM RUNNING"

# =========================
# API DECISION (CORE)
# =========================
@app.route("/api/decision", methods=["POST"])
def decision():
    data = request.json
    user_input = data.get("input", "")

    # 🔥 ตรงนี้พี่จะเอา ENGINE จริงมาเสียบทีหลัง
    response = f"[AI]: วิเคราะห์ -> {user_input}"

    return jsonify({
        "status": "ok",
        "input": user_input,
        "output": response
    })

# =========================
# WALLET API (เชื่อมของพี่)
# =========================
@app.route("/wallet/topup", methods=["POST"])
def wallet_topup():
    data = request.json
    email = data.get("email")
    amount = data.get("amount")

    return jsonify({
        "status": "success",
        "message": f"Topup {amount} to {email}"
    })

# =========================
# SERVE STATIC (Render)
# =========================
@app.route("/app")
def serve_app():
    return send_from_directory("static", "index.html")

# =========================
# STATIC FILES
# =========================
@app.route("/static/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)

# =========================
# RUN LOCAL
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
