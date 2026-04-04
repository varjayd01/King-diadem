import time

def analyze_human(context):
    energy = context.get("energy", 50)          # แรงใจ / แรงกาย
    money = context.get("money", 0)             # ทรัพยากร
    stress = context.get("stress", 50)          # ความกดดัน
    risk_tolerance = context.get("risk", 0.5)   # รับความเสี่ยงได้แค่ไหน

    # 🔥 entropy = ความเสื่อมของมนุษย์
    entropy = (stress * 0.6) + ((100 - energy) * 0.4)

    state = "stable"

    if entropy > 70:
        state = "overload"
    elif entropy < 30:
        state = "optimal"

    return {
        "domain": "human",
        "timestamp": time.time(),
        "energy": energy,
        "money": money,
        "stress": stress,
        "entropy": entropy,
        "state": state
    }
