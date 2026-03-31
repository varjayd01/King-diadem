import os
from google import genai

from core.brain import run_brain

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)


class KingDiademEngine:

    def call_gemini(self, text):
        try:
            res = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=text
            )
            return res.text
        except Exception as e:
            return f"AI ERROR: {str(e)}"

    # 🟢 CHAT MODE (AI คุยจริง)
    def chat_mode(self, text):
        ai = self.call_gemini(text)

        if not ai or "ERROR" in ai:
            return "⚠️ AI ไม่ตอบ"

        return ai

    # 🔴 DECISION MODE
    def decision_mode(self, text):
        return run_brain(text)

    # 🔥 ROUTER (ตัวเดียวจบ)
    def run(self, text, mode="chat"):

        if mode == "chat":
            return {
                "type": "chat",
                "reply": self.chat_mode(text)
            }

        if mode == "decision":
            result = self.decision_mode(text)
            return {
                "type": "decision",
                "reply": result
            }

        return {
            "type": "chat",
            "reply": "unknown mode"
        }
