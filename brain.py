import os
import requests

try:
    from google import genai
except Exception:
    genai = None

GEMINI_KEY = (
    os.getenv("GEMINI_API_KEY") or
    os.getenv("GEMINI_API_KEY2")
)


def ask_gemini(message):
    if genai is None:
        return "[Gemini SDK not installed]"

    if not GEMINI_KEY:
        return "[Gemini key missing]"

    client = genai.Client(api_key=GEMINI_KEY)

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[
                {
                    "parts": [
                        {"text": message}
                    ]
                }
            ]
        )
        return getattr(response, "text", str(response))
    except Exception as e:
        return f"[Gemini error] {e}"


# ===== MASTER BRAIN =====
def run_brain(message):

    # 👉 ตรงนี้คือ “ตัวเลือกเส้นทาง”
    # อนาคตใส่:
    # - KING_DIadem
    # - Gemini
    # - Memory

    return ask_gemini(message)
