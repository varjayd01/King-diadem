def run_brain(message):

    if not message:
        return {"text":"ไม่มีข้อมูล","risk":0,"choices":[]}

    risk = 0.2

    if "เสี่ยง" in message:
        risk = 0.8

    if risk >= 0.95:
        return {
            "text":"⛔ STOP",
            "risk":risk,
            "choices":["หยุด","ถอย","ออก"]
        }

    return {
        "text":f"วิเคราะห์: {message}",
        "risk":risk,
        "choices":["A","B","C"]
    }
