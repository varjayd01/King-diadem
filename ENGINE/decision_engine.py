def decision_intelligence(state, risk):

    if risk["risk_score"] > 70:
        return {"action": "stabilize", "message": "ลดความเสี่ยงทันที"}

    if state["resource"] < 30:
        return {"action": "recover_resource", "message": "เพิ่มทรัพยากร"}

    return {"action": "maintain", "message": "รักษาสถานะ"}
