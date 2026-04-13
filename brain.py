import os
import requests

OPENAI_API_KEY = os.getenv("CHATGPT_API_KEY")

def ask_openai(message):
    url = "https://api.openai.com/v1/responses"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4.1-mini",
        "input": message
    }

    r = requests.post(url, headers=headers, json=data)

    try:
        return r.json()["output"][0]["content"][0]["text"]
    except:
        return str(r.text)


# ===== MASTER BRAIN =====
def run_brain(message):

    # 👉 ตรงนี้คือ “ตัวเลือกเส้นทาง”
    # อนาคตใส่:
    # - KING_DIadem
    # - Gemini
    # - Memory

    return ask_openai(message)
