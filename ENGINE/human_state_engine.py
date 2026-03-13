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


def evaluate_human_state(food, money, risk):

    score = 50

    if food < 2:
        score -= 20

    if money < 100:
        score -= 10

    if risk > 5:
        score -= 20

    return score
