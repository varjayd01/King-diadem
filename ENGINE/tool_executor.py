# ENGINE/tool_executor.py

def execute_tool(decision: dict):
    action = decision.get("action", "")

    # -------------------------
    # TOOL MAPPING
    # -------------------------
    if action == "open_url":
        return {
            "tool": "browser",
            "status": "executed",
            "result": f"Opening {decision.get('url')}"
        }

    elif action == "write_note":
        with open("data/notes.txt", "a") as f:
            f.write(decision.get("content", "") + "\n")

        return {
            "tool": "file_system",
            "status": "saved"
        }

    elif action == "calculate":
        result = eval(decision.get("expression", "0"))
        return {
            "tool": "calculator",
            "result": result
        }

    # -------------------------
    # DEFAULT
    # -------------------------
    return {
        "tool": "none",
        "status": "no_action"
    }
