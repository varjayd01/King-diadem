# ENGINE/king_response.py

def king_response(user_input: str, consensus_json: str) -> str:
    import json
    try:
        consensus = json.loads(consensus_json)
    except Exception:
        consensus = {}

    action = consensus.get("final_action", "maintain")
    confidence = consensus.get("confidence", 50)
    message = consensus.get("message", "")

    lines = [
        "[KING DIADEM — Decision Output]",
        "",
        f"Action: {action.upper()}",
        f"Confidence: {confidence}%",
    ]
    if message:
        lines.append(f"Note: {message}")

    lines += [
        "",
        f"Input assessed: {user_input[:120]}",
        "",
        "— Fail Less. Harm Less. Restore Choice. —",
    ]

    return "\n".join(lines)
