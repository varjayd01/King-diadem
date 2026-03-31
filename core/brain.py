# core/brain.py

def decision_engine(message: str):

    if not message or message.strip() == "":
        return {
            "text": "ไม่มีข้อมูล",
            "risk": 0,
            "choices": []
        }

    risk = 0.2
    choices = []

    if "เสี่ยง" in message:
        risk = 0.8
        choices = ["หยุด", "ถอย", "หาทางใหม่"]

    elif "เงิน" in message:
        risk = 0.5
        choices = ["เก็บ", "ลดรายจ่าย", "ลงทุนแบบระวัง"]

    else:
        choices = ["A", "B", "C"]

    return {
        "text": f"วิเคราะห์: {message}",
        "risk": risk,
        "choices": choices
    }


def run_brain(message: str):
    return decision_engine(message)
