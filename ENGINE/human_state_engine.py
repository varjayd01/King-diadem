def analyze_human_state(text):

    text = text.lower()

    state = {
        "depression": False,
        "fear": False,
        "dependency": False,
        "violence_risk": False
    }

    if "depress" in text or "หมดหวัง" in text:
        state["depression"] = True

    if "กลัว" in text or "fear" in text:
        state["fear"] = True

    if "ต้องเลี้ยงเขา" in text:
        state["dependency"] = True

    if "ทำร้าย" in text or "violence" in text:
        state["violence_risk"] = True

    return state
