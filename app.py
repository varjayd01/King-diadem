from flask import Flask, request, jsonify, send_from_directory
from core.orchestrator import Orchestrator

app = Flask(__name__, static_folder="static")
system = Orchestrator()

@app.route("/")
def home():
    return send_from_directory("static", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    msg = data.get("message")

    reply = system.process(msg)

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
