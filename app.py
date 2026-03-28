from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "KING DIADEM RUNNING"

@app.route("/api/decision", methods=["POST"])
def decision():
    data = request.json
    user_input = data.get("input")

    # TEMP: test ก่อน
    response = f"คุณพิมพ์ว่า: {user_input}"

    return jsonify({"output": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
