from flask import Flask, request, jsonify
from ENGINE.universal_engine import run_engine

app = Flask(__name__)

@app.route("/")
def home():
    return open("static/index.html").read()

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.json or {}
        result = run_engine(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
