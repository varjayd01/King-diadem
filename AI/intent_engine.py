def detect_intent(text):

    t = text.lower()

    if "เครียด" in t or "หมดทาง" in t:
        return "survivor"

    if "ทำยังไงดี" in t:
        return "seeker"

    if "วิเคราะห์" in t:
        return "strategist"

    if "สร้าง" in t:
        return "builder"

    return "explorer"
