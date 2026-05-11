# core/fate_core.py
"""
FATE CORE — Deterministic + Human-Aware
Bridge: LLM Capability → FATE Framework → Human Decision Quality
"""

SYSTEM_MODE = "DETERMINISTIC_LOGIC_ONLY"

CRISIS_SIGNALS = ["ฆ่า","ตาย","ไม่อยากอยู่","พังหมด","จบแล้ว","หมดแล้ว"]

def run_fate(input_data: dict) -> dict:
    if not input_data or not isinstance(input_data, dict):
        return _reject("INVALID_INPUT")
    if "message" not in input_data:
        return _reject("MISSING_MESSAGE")
    if not isinstance(input_data["message"], str):
        return _reject("INVALID_TYPE")

    message = input_data["message"].strip()
    if not message:
        return _reject("EMPTY_INPUT")

    normalized = {"message": message}
    risk = detect_human_risk(message)

    trace = {
        "rules": ["INPUT_VALIDATION", "NORMALIZATION", "RISK_SCAN"],
        "risk_level": risk
    }

    if risk == "critical":
        return {
            "status": "block",
            "reason": "HIGH_RISK",
            "safe_response": safe_response(),
            "trace": trace,
            "hotline": "1323"
        }

    # Run civil work evaluation if tasks provided
    civil_result = None
    if "tasks" in input_data:
        try:
            from core.civil_work_core import evaluate_work_plan
            civil_result = evaluate_work_plan(input_data["tasks"])
        except Exception as e:
            civil_result = {"error": str(e)}

    # Run dependency cycle analysis
    cycle_result = None
    if "state" in input_data:
        try:
            from core.dependency_cycle import dependent_cycle
            cycle_result = dependent_cycle(input_data["state"])
        except Exception as e:
            cycle_result = {"error": str(e)}

    return {
        "status": "pass",
        "data": normalized,
        "risk": risk,
        "trace": trace,
        "civil": civil_result,
        "cycle": cycle_result
    }

def detect_human_risk(text: str) -> str:
    for w in CRISIS_SIGNALS:
        if w in text:
            return "critical"
    if len(text) < 3:
        return "low"
    return "normal"

def safe_response() -> str:
    return (
        "สถานการณ์นี้มีความเสี่ยงสูง\n"
        "แนะนำให้หยุดก่อน และคุยกับคนที่ไว้ใจได้ทันที\n"
        "สายด่วนสุขภาพจิต: 1323 (ฟรี 24 ชม.)"
    )

def _reject(reason: str) -> dict:
    return {"status": "reject", "reason": reason}
