import os
from google import genai

from core.brain import run_brain

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)


class KingDiademEngine:

    # ------------------------
    # 🔌 AI LAYER (มี fallback)
    # ------------------------
    def call_gemini(self, text):
        try:
            res = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=text
            )
            return res.text
        except Exception:
            return None  # ❗ไม่ return ERROR string

    def safe_fallback(self, text):
        return {
            "status": "fallback",
            "options": [
                "ลองใหม่อีกครั้ง",
                "ลดความซับซ้อนของคำถาม",
                "หยุดพัก (SYSTEM PAUSE)"
            ]
        }

    # ------------------------
    # 🧠 HUMAN PROTOCOL
    # ------------------------
    def enforce_human_protocol(self, ai_text):
        # ถ้า AI ตอบสั้น/ไม่ปลอดภัย → เติม choice
        return {
            "options": [
                f"แนวทางที่ 1: {ai_text}",
                "แนวทางที่ 2: ลองอีกวิธีที่ปลอดภัยกว่า",
                "Fallback: หยุดก่อนแล้วประเมินใหม่"
            ],
            "note": "ระบบรักษาทางเลือก (Choice > 0)"
        }

    # ------------------------
    # 💬 CHAT MODE
    # ------------------------
    def chat_mode(self, text):
        ai = self.call_gemini(text)

        if not ai:
            return self.safe_fallback(text)

        return self.enforce_human_protocol(ai)

    # ------------------------
    # 🔴 DECISION MODE
    # ------------------------
    def decision_mode(self, text):
        try:
            result = run_brain(text)

            # ❗ guard ถ้า brain พัง
            if not result:
                return self.safe_fallback(text)

            return result

        except Exception:
            return self.safe_fallback(text)

    # ------------------------
    # 🚦 ROUTER (ศูนย์กลางเดียว)
    # ------------------------
    def run(self, text, mode="chat"):

        if mode == "chat":
            return {
                "type": "chat",
                "data": self.chat_mode(text)
            }

        if mode == "decision":
            return {
                "type": "decision",
                "data": self.decision_mode(text)
            }

        # ❗ default fallback
        return {
            "type": "fallback",
            "data": self.safe_fallback(text)
        }
