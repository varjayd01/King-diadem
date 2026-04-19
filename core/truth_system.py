import os, asyncio
from openai import AsyncOpenAI

# 🔥 ใช้ตัวใหม่
try:
    from google import genai
except:
    genai = None

from ENGINE.realhuman_survivorengine import RealHumanSurvivorEngine, HumanState


KERNEL_PROMPT = """
[SYSTEM: ETERNAL TRUTH MODE]
สะท้อนความจริง + ให้ทางเลือกที่รอดจริงเท่านั้น
"""


class TruthSystem:
    def __init__(self):
        self.keys = {
            "gpt": os.getenv("CHATGPT_API_KEY"),
            "gemini": os.getenv("GEMINI_API_KEY")
        }

    async def gpt_view(self, context):
        try:
            client = AsyncOpenAI(api_key=self.keys["gpt"])
            res = await client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": context}]
            )
            return res.choices[0].message.content
        except Exception as e:
            return f"[GPT FAIL] {str(e)}"

    async def gemini_view(self, context):
        if genai is None:
            return "[Gemini not installed]"

        try:
            client = genai.Client(api_key=self.keys["gemini"])
            res = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=context
            )
            return res.text
        except Exception as e:
            return f"[Gemini FAIL] {str(e)}"


async def run_truth_infrastructure(user_input, state_dict):

    # ✅ 1. Survivor
    try:
        survivor = RealHumanSurvivorEngine()
        h_state = HumanState(**state_dict)
        survival_out = survivor.run(h_state)

        survival_json = {
            "status": str(survival_out.status),
            "actions": str(survival_out.actions)
        }

    except Exception as e:
        survival_json = {"error": str(e)}

    # ✅ 2. Context
    context = f"""
    สถานะ: {survival_json}
    เหตุการณ์: {user_input}
    """

    ts = TruthSystem()

    # ✅ 3. Run parallel (กันพังแยก)
    results = await asyncio.gather(
        ts.gpt_view(context),
        ts.gemini_view(context),
        return_exceptions=True
    )

    return {
        "survival": survival_json,
        "perspectives": results
    }
