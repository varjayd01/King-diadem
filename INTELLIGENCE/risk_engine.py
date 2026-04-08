def evaluate_risk(user_input: str):
    text = (user_input or "").lower()

    score = 0.1

    if any(k in text for k in ["เจ็บ", "ทำร้าย", "เลือด", "ไฟ"]):
        score = 0.9
    elif any(k in text for k in ["ล้ม", "เสี่ยง"]):
        score = 0.6

    level = "low"
    if score > 0.7:
        level = "high"
    elif score > 0.4:
        level = "medium"

    return {
        "risk_score": score,
        "risk_level": level
    }
