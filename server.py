from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder="static")

# ===== CORE LOGIC (Minimal Kernel) =====
def process_input(user_input):
    if not user_input:
        return "คุณยังไม่ได้พิมพ์อะไร"

    # SIMPLE SCL-7 STYLE RESPONSE
    return f"""
[รับสภาพ]
สิ่งที่คุณกำลังคิด มันมีน้ำหนักจริง

[โครงสร้าง]
ตอนนี้สิ่งที่เกิดขึ้นคือ:
{user_input}

[ทางเลือก]
คุณยังไม่จำเป็นต้องรีบตัดสินใจ
ลองอยู่กับมันก่อนก็ได้
"""

# ===== API =====
@app.route("/api/process", methods=["POST"])
def process():
    data = request.json
    user_input = data.get("input", "")

    result = process_input(user_input)

    return jsonify({"output": result})


# ===== FRONTEND =====
@app.route("/")
def index():
    return send_from_directory("static", "index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
