import os
import asyncio

# 🔒 OpenAI ใหม่
from openai import AsyncOpenAI

# 🔒 Google GenAI ใหม่ (แทน generativeai)
try:
    from google import genai
except Exception as e:
    genai = None
    print("GENAI IMPORT ERROR:", e)


# --- LYLA LOGIC CORE ---
TRUTH_PROMPT = """
[SYSTEM COMMAND: ETERNAL TRUTH MODE]
- บรรยายความจริงตามสภาพที่เกิดขึ้น
- รักษา Choice(t) > 0 เสมอ
- ไม่สั่ง ไม่ชี้นำ ไม่ตัดสิน
- สรุปท้าย 3 บรรทัด

[FORMAT]
- การปรากฏของความจริง:
- [สรุปความจริงเพื่อการใช้งาน]:
"""


# 🔥 MAIN ENGINE
async def run_truth_engine(user_input, resource):

    # 🔑 ENV
    gpt_key = os.getenv("CHATGPT_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")

    # 🧠 SAFE GPT
    async def get_gpt_view():
        if not gpt_key:
            return "[GPT NOT CONFIGURED]"

        try:
            client = AsyncOpenAI(api_key=gpt_key)

            res = await client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": TRUTH_PROMPT},
                    {"role": "user", "content": user_input}
                ]
            )
            return res.choices[0].message.content

        except Exception as e:
            return f"[GPT ERROR] {str(e)}"

    # 🧠 SAFE GEMINI
    async def get_gemini_view():
        if genai is None:
            return "[GENAI NOT INSTALLED]"

        if not gemini_key:
            return "[GEMINI KEY MISSING]"

        try:
            client = genai.Client(api_key=gemini_key)

            res = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=f"{TRUTH_PROMPT}\n\nสถานการณ์:\n{user_input}"
            )

            return res.text

        except Exception as e:
            return f"[GEMINI ERROR] {str(e)}"

    # ⚡ RUN PARALLEL (ไม่ให้พังทั้งระบบ)
    results = await asyncio.gather(
        get_gpt_view(),
        get_gemini_view(),
        return_exceptions=True
    )

    # 🔒 SAFE RESOURCE → RISK
    try:
        resource_value = float(resource)
    except:
        resource_value = 50  # fallback กลาง

    risk_index = max(0, min(100, (100 - resource_value) * 0.75))

    # 📦 OUTPUT (JSON SAFE 100%)
    return {
        "view_structural": str(results[0]),
        "view_possibility": str(results[1]),
        "view_stability": "Fallback stability channel active",
        "risk_index": risk_index
    }
