# ENGINE/consensus_engine.py

def consensus_engine(council_result, state=None):
    state = state or {}
    decision = council_result.get("decision", {})
    votes = council_result.get("votes", [])

    tally = {}
    for vote in votes:
        action = vote.get("action", decision.get("action", "maintain"))
        tally[action] = tally.get(action, 0) + float(vote.get("score", 0))

    if tally:
        final_action = max(tally, key=tally.get)
    else:
        final_action = decision.get("action", "maintain")

    confidence = round(min(100.0, max(0.0, float(council_result.get("score", 50)))), 2)

    return {
        "final_action": final_action,
        "message": decision.get("message", ""),
        "confidence": confidence,
        "tally": tally,
        "voters": len(votes),
    }
