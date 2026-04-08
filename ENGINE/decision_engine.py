from AI.intent_engine import analyze_intent
from INTELLIGENCE.risk_engine import evaluate_risk

def decision_mode(self, text):
    try:
        intent = analyze_intent(text)
        risk = evaluate_risk(text)

        # 🔥 ใช้ key จริงของพี่
        if risk["risk_level"] == "high":
            return "⚠️ เสี่ยงเกินไป หยุดก่อน"

        if intent == "survival":
            return "🛡️ เอาตัวรอดก่อน ลดรายจ่าย เพิ่มเงิน"

        if intent == "question":
            return "🤔 ต้องการข้อมูลเพิ่ม"

        return "✅ ทำได้ แต่คิดก่อน"

    except Exception as e:
        return f"❌ ERROR: {str(e)}"
