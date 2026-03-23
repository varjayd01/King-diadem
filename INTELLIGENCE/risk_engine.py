def evaluate_risk(user_input: str):
    text = (user_input or "").lower()

    score = 0.1

    if any(k in text for k in ["ฆ่า", "ทำร้าย", "หลอก", "โกง"]):
        score = 0.9
    elif any(k in text for k in ["ลงทุน", "เสี่ยง"]):
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
