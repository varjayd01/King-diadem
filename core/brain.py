# core/brain.py

import re

# -----------------------------
# CONFIG
# -----------------------------
RISK_KEYWORDS = {
    "เสี่ยง": 0.8,
    "อันตราย": 0.9,
    "หนี้": 0.7,
    "ลงทุน": 0.6,
    "พนัน": 0.95,
    "ทะเลาะ": 0.7,
    "เลิก": 0.8,
}

SAFE_KEYWORDS = {
    "เก็บเงิน": -0.2,
    "วางแผน": -0.3,
    "เรียน": -0.2,
}

# -----------------------------
# CORE ANALYSIS
# -----------------------------
def analyze_risk(text: str):
    risk = 0.2  # base

    for word, score in RISK_KEYWORDS.items():
        if word in text:
            risk += score

    for word, score in SAFE_KEYWORDS.items():
        if word in text:
            risk += score

    # clamp 0-1
    return max(0, min(1, risk))


def extract_intent(text: str):
    text = text.lower()

    if any(w in text for w in ["เงิน", "ลงทุน", "รายได้"]):
        return "finance"

    if any(w in text for w in ["รัก", "แฟน", "เลิก"]):
        return "relationship"

    if any(w in text for w in ["งาน", "อาชีพ"]):
        return "career"

    return "general"


# -----------------------------
# DECISION LOGIC
# -----------------------------
def generate_choices(intent, risk):

    if risk > 0.85:
        return [
            "หยุดทันที",
            "ถอยออกจากสถานการณ์",
            "หาทางเลือกใหม่ที่ปลอดภัย"
        ]

    if intent == "finance":
        return [
            "เก็บเงิน",
            "ลงทุนแบบความเสี่ยงต่ำ",
            "ศึกษาข้อมูลก่อนตัดสินใจ"
        ]

    if intent == "relationship":
        return [
            "สื่อสารตรงไปตรงมา",
            "ให้เวลาและพื้นที่",
            "ประเมินความสัมพันธ์ใหม่"
        ]

    if intent == "career":
        return [
            "พัฒนาทักษะเพิ่ม",
            "หาทางเลือกงานใหม่",
            "วางแผนระยะยาว"
        ]

    return [
        "คิดก่อนทำ",
        "ประเมินความเสี่ยง",
        "เลือกทางที่ไม่ทำร้ายตัวเอง"
    ]


def stop_the_line(risk):
    return risk >= 0.95


# -----------------------------
# MAIN ENGINE
# -----------------------------
def decision_engine(message: str):

    if not message or message.strip() == "":
        return {
            "text": "ไม่มีข้อมูลให้วิเคราะห์",
            "risk": 0,
            "intent": "none",
            "choices": []
        }

    risk = analyze_risk(message)
    intent = extract_intent(message)

    # 🔥 STOP THE LINE
    if stop_the_line(risk):
        return {
            "text": "⛔ ความเสี่ยงสูงมาก หยุดก่อน",
            "risk": risk,
            "intent": intent,
            "choices": [
                "หยุดทุกการตัดสินใจ",
                "ถอยออกทันที",
                "ขอความช่วยเหลือ"
            ]
        }

    choices = generate_choices(intent, risk)

    return {
        "text": f"วิเคราะห์แล้ว ({intent})",
        "risk": round(risk, 2),
        "intent": intent,
        "choices": choices
    }


# -----------------------------
# ENTRY POINT
# -----------------------------
def run_brain(message: str):
    return decision_engine(message)
