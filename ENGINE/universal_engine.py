# ENGINE/universal_engine.py

from ENGINE.pattern_engine import analyze_pattern
from ENGINE.risk_engine import analyze_risk
from ENGINE.decision_engine import decision_intelligence
from ENGINE.council_engine import council_engine
from ENGINE.consensus_engine import consensus_engine
from core.emptiness_guard import emptiness_guard


def _normalize_input(payload):
    if not isinstance(payload, dict):
        payload = {}

    return {
        "input": str(payload.get("input", payload.get("question", ""))).strip(),
        "entropy": payload.get("entropy", 40),
        "resource": payload.get("resource", 50),
        "stability": payload.get("stability", 60),
        "choices": payload.get("choices", 1),
        "confidence": payload.get("confidence", 0.5),
        "decision": payload.get("decision"),
        "previous_decision": payload.get("previous_decision"),
        "decision_history": payload.get("decision_history", []),
        "warnings": payload.get("warnings", []),
        "alternatives": payload.get("alternatives", []),
        "locked": payload.get("locked", False),
    }


def run_engine(payload):
    raw = _normalize_input(payload)

    pattern = analyze_pattern(raw)
    core_state = {**raw, **pattern}

    core_state = emptiness_guard(core_state)

    risk = analyze_risk(core_state)
    decision = decision_intelligence(core_state, risk)
    council = council_engine(decision, core_state)
    consensus = consensus_engine(council, core_state)

    packet = {
        "status": "ok",
        "input": raw,
        "state": core_state,
        "risk": risk,
        "decision": decision,
        "council": council,
        "consensus": consensus,
    }

    packet = emptiness_guard({**packet, **core_state})

    if packet.get("blocked"):
        return {
            "status": "blocked",
            "reason": packet.get("reason"),
            "output": packet.get("output", {}),
            "state": packet.get("state", {}),
            "risk": packet.get("risk", {}),
            "decision": packet.get("decision", {}),
            "council": packet.get("council", {}),
            "consensus": packet.get("consensus", {}),
        }

    return {
        "status": "ok",
        "output": packet.get("output", {}),
        "state": packet.get("state", {}),
        "risk": packet.get("risk", {}),
        "decision": packet.get("decision", {}),
        "council": packet.get("council", {}),
        "consensus": packet.get("consensus", {}),
    }
