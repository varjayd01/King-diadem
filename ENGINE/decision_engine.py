def ENGINE_DECISION(text: str):

    if "น้อย" in text or "0" in text:
        return {"mode": "SURVIVAL", "action": "save"}

    if "เสี่ยง" in text or "9" in text:
        return {"mode": "DEFENSE", "action": "avoid"}

    return {"mode": "NORMAL", "action": "proceed"}
