import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai  # ต้องมีตัวนี้ใน requirements.txt นะตะ

load_dotenv()

app = Flask(__name__)

# ---------------------------------------------------------
# [AI CONFIG] เชื่อมต่อกับ Google AI Studio
# ---------------------------------------------------------
# ดึง Key ที่พี่ตั้งไว้ใน Render มาใช้งาน
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash') # หรือรุ่นที่พี่ถนัด

def lyla_logic_process(user_msg):
    # ใส่ System Prompt ของพี่ลงไปที่นี่เพื่อให้ AI ไม่รันมโนอดีต
    prompt = f"ในฐานะ LYLA KERNEL จอมทัพสั่งว่า: {user_msg}"
    response = model.generate_content(prompt)
    return response.text

# ---------------------------------------------------------
# [ROUTES]
# ---------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/v1/chat', methods=['POST'])
def chat():
    data = request.json
    msg = data.get('message', '')
    
    # รัน AI ด้วย Key จาก Google AI Studio
    try:
        ai_response = lyla_logic_process(msg)
    except Exception as e:
        ai_response = f"FAILED: ระบบเชื่อมต่อ API ขัดข้องเนื่องจาก {e}"

    return jsonify({
        "operator": "LYLA KERNEL",
        "response": ai_response
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
