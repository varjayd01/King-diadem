# core/orchestrator.py

import os
from core.king_diadem_core import king_diadem_decision
from core.memory_store import log_decision
from google import genai

# ===== INIT GEMINI (NEW SDK) =====
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-1.5-pro"


class Orchestrator:

    def __init__(self):
        pass

    def run(self, user_input, context=None):
        try:
            # ===== STEP 1: SYSTEM DECISION =====
            decision = king_diadem_decision(
                location=context.get("location", "unknown"),
                lat=context.get("lat", 0),
                lng=context.get("lng", 0),
                food=context.get("food", 0),
                money=context.get("money", 0),
                risk=context.get("risk", 0),
            )

            # ===== STEP 2: BUILD PROMPT =====
            prompt = f"""
You are KING DIADEM AI.

User Input:
{user_input}

System Decision:
{decision}

Rules:
- Be clear
- Be direct
- No fluff
- Preserve user choice

Answer:
"""

            # ===== STEP 3: CALL GEMINI =====
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )

            reply = response.text if response.text else "No response"

            # ===== STEP 4: MEMORY LOG =====
            log_decision({
                "user_input": user_input,
                "decision": decision,
                "reply": reply
            })

            return {
                "status": "success",
                "reply": reply,
                "decision": decision
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
