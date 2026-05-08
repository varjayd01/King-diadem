# ENGINE/intent_engine.py

def analyze_intent(text: str) -> dict:
    text_lower = text.lower()

    if any(k in text_lower for k in ["พัง", "ล้ม", "crisis", "collapse", "หมด"]):
        return {"intent": "collapse_prevention", "confidence": 0.9}
    elif any(k in text_lower for k in ["เสี่ยง", "risk", "อันตราย", "danger"]):
        return {"intent": "risk_assessment", "confidence": 0.8}
    elif any(k in text_lower for k in ["รอด", "survive", "อยู่รอด", "ขาด"]):
        return {"intent": "survival", "confidence": 0.85}
    elif any(k in text_lower for k in ["เลือก", "decide", "ตัดสิน", "choice"]):
        return {"intent": "decision_support", "confidence": 0.75}
    else:
        return {"intent": "general_governance", "confidence": 0.6}
