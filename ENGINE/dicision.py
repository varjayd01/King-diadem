def think(text: str):
    if "หิว" in text:
        return "ไปกินก่อน เดี๋ยวพังทั้งระบบ"

    if "เหนื่อย" in text:
        return "พักก่อน แล้วค่อยกลับมาใหม่"

    return f"รับแล้ว: {text}"
