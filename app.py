def decision_engine(user_input, persona):
    if not user_input:
        return "พิมพ์ก่อนค่ะ"

    style = persona.get("style", "normal")

    if style == "fun":
        return f"✨ วันนี้ต้องปังนะคะ: {user_input}"

    elif style == "deep":
        return f"""
🧠 โหมดผู้เชี่ยวชาญ

- วิเคราะห์: {user_input}
- มองระยะยาว
- ลดความเสี่ยง
- เลือกทางที่รอด

สรุป: เลือกสิ่งที่ “ไม่พังก่อน”
"""

    else:
        return f"📌 ระบบคิดว่า: {user_input}"
