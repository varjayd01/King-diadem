import os
from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI

app = Flask(__name__, static_folder="static")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return send_from_directory("static", "index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    prompt = data.get("message", "")

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a survival decision AI."},
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message.content
        return jsonify({"reply": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
