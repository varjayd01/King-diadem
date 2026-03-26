from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='static')


# ======================
# ROUTE: HOME
# ======================
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


# ======================
# CORE: DECISION ENGINE
# ======================
def decision_engine(user_input):
    text = user_input.lower()

    # ===== Survival Mode =====
    if "หิว" in text or "ไม่ได้กิน" in text:
        return {
            "mode": "survival",
            "result": "ไปกินอะไรก่อนทันที อย่าฝืน ระบบไม่ให้คิดต่อถ้ายังหิว"
        }

    if "ไม่มีเงิน" in text or "จน" in text:
        return {
            "mode": "survival",
            "result": "ลดรายจ่ายทันที + หาเงินระยะสั้นก่อน เช่น งานรายวัน / ขายของ / รับจ้าง"
        }

    if "เครียด" in text or "ท้อ" in text:
        return {
            "mode": "stabilize",
            "result": "หยุดก่อน หายใจลึก 5 ครั้ง แล้วค่อยตัดสินใจ อย่าฝืนตอนสติไม่เต็ม"
        }

    # ===== Risk Detection =====
    if "เมา" in text or "ไม่ปลอดภัย" in text:
        return {
            "mode": "danger",
            "result": "เรียกรถกลับทันที อย่าอยู่ต่อ ความปลอดภัยมาก่อน"
        }

    # ===== Default Thinking =====
    return {
        "mode": "normal",
        "result": f"วิเคราะห์แล้ว: {user_input}"
    }


# ======================
# ROUTE: DECISION
# ======================
@app.route('/decision', methods=['POST'])
def decision():
    data = request.get_json()

    if not data or "input" not in data:
        return jsonify({
            "status": "error",
            "message": "No input provided"
        }), 400

    user_input = data.get("input", "")

    result = decision_engine(user_input)

    return jsonify({
        "status": "success",
        "mode": result["mode"],
        "result": result["result"]
    })


# ======================
# HEALTH CHECK
# ======================
@app.route('/health')
def health():
    return "OK", 200


# ======================
# RUN LOCAL ONLY
# ======================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
