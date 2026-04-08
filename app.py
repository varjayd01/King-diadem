from flask import Flask, render_template, request, jsonify
from engine.decision_engine import decide, seed_reply

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json(force=True) or {}
    message = (data.get("message") or "").strip()
    seed = (data.get("seed") or "").strip()

    if not message:
        return jsonify({"reply": "พิมพ์อะไรสักอย่างก่อนสิพี่ 😏"})

    reply = decide(message, seed=seed)
    return jsonify({"reply": reply})

@app.route("/api/seed", methods=["POST"])
def api_seed():
    data = request.get_json(force=True) or {}
    seed = (data.get("seed") or "").strip()
    return jsonify({"reply": seed_reply(seed)})

if __name__ == "__main__":
    app.run(debug=True)
