import os, asyncio
from openai import AsyncOpenAI

try:
    from google import genai
except:
    genai = None


class TruthSystem:
    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.gemini_keys = [
            os.getenv("GEMINI_API_KEY1"),
            os.getenv("GEMINI_API_KEY2")
        ]

    async def gpt_view(self, context):
        try:
            client = AsyncOpenAI(api_key=self.openai_key)

            res = await client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": context}]
            )

            return res.choices[0].message.content

        except Exception as e:
            return f"[GPT ERROR] {str(e)}"

    async def gemini_view(self, context):
        if genai is None:
            return "[Gemini not installed]"

        for key in self.gemini_keys:
            if not key:
                continue

            try:
                client = genai.Client(api_key=key)

                res = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=context
                )

                return res.text

            except Exception:
                continue

        return "[Gemini ERROR all keys failed]"


async def run_truth(user_input, state):
    context = f"""
    STATE: {state}
    INPUT: {user_input}
    """

    ts = TruthSystem()

    results = await asyncio.gather(
        ts.gpt_view(context),
        ts.gemini_view(context),
        return_exceptions=True
    )

    return {
        "gpt": str(results[0]),
        "gemini": str(results[1])
    }


def run_sync(user_input, state):
    return asyncio.run(run_truth(user_input, state))
