# ENGINE/strategy_planner.py

def plan(pattern: dict) -> dict:
    entropy = pattern.get("entropy", 40)
    resource = pattern.get("resource", 50)
    stability = pattern.get("stability", 60)
    user_input = pattern.get("input", "")

    if entropy > 70 or resource < 30:
        strategy = "STABILIZE"
        actions = ["หยุดการขยายตัว", "รักษาทรัพยากรที่มี", "ลด exposure ทันที"]
    elif stability < 40:
        strategy = "RESTORE"
        actions = ["ประเมินจุดพัง", "หาแหล่งสนับสนุน", "สร้าง fallback path"]
    else:
        strategy = "OPTIMIZE"
        actions = ["เดินหน้าอย่างระมัดระวัง", "ติดตาม drift รายวัน", "รักษา waterline"]

    return {
        "strategy": strategy,
        "actions": actions,
        "entropy": entropy,
        "resource": resource,
        "stability": stability,
        "message": f"Strategy: {strategy} — Fail Less. Harm Less. Restore Choice.",
        "risk_score": max(0, (entropy - resource) / 2)
    }
