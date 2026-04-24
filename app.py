from flask import Flask, request, jsonify, send_from_directory
from ENGINE.decision_engine import run_decision

app = Flask(__name__, static_folder="static", static_url_path="")

# 🌐 หน้าเว็บหลัก
@app.route("/")
def index():
    return send_from_directory("static", "index.html")

# 🧠 API เรียก Decision Engine
@app.route("/api/decision", methods=["POST"])
def decision():
    data = request.get_json()
    result = run_decision(data)
    return jsonify(result)

# 🚀 RUN
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
