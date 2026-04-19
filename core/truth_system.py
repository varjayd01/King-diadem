import os, asyncio, openai, google.generativeai as genai
from ENGINE.realhuman_survivorengine import RealHumanSurvivorEngine, HumanState

# LYLA OPEN SYSTEM CORE LOGIC KERNEL (K1-K14 Integrated)
KERNEL_PROMPT = """
[SYSTEM: ETERNAL TRUTH MODE - KERNEL GATES K1-K14 ACTIVATED]
1. ห้ามแทนตัวด้วยสรรพนามใดๆ (No ผม/เรา/คิง/ไลล่า) และห้ามเรียกผู้ใช้ (No คุณ/ท่าน/มนุษย์)
2. บรรยาย "ความจริงที่ปรากฏ" ตามสัจธรรมและหลักฐาน (Evidence ON, Ego OFF)
3. รันข้อมูลผ่าน Runtime Gates: K1(Reality), K2(Compassion), K4(Floor Restoration), K13(Stop-the-Line)
4. กฎเหล็ก: Choice(t) must always be > 0. หากทางเลือกเหลือ 1 ให้เข้าสู่ Protective Mode
5. ไม่ชี้นำ ไม่สั่ง ไม่สอน ไม่ตัดสิน ให้เพียง "สะท้อนความจริง" และ "กางทางเลือกที่รอดจริง"
6. ท้ายแชทต้องมีส่วน [สรุปความจริงเพื่อการใช้งาน] 3 บรรทัดจบเสมอ

[CONTEXT]
- Measure Daily Harm Delta (DHD). Identify Drift before Collapse.
- Stabilize before Optimize.
"""

class TruthSystem:
    def __init__(self):
        self.keys = {
            "gpt": os.getenv("CHATGPT_API_KEY"),
            "studio": os.getenv("GEMINI_API_KEY1"),
            "cloud": os.getenv("GEMINI_API_KEY2")
        }

    async def get_view(self, key, model, context, perspective_name):
        try:
            full_prompt = f"{KERNEL_PROMPT}\n\n[สถานการณ์ปัจจุบัน]\n{context}"
            if "gpt" in model:
                client = openai.AsyncOpenAI(api_key=key)
                res = await client.chat.completions.create(
                    model="gpt-4o", messages=[{"role": "system", "content": full_prompt}]
                )
                return res.choices[0].message.content
            else:
                genai.configure(api_key=key)
                m = genai.GenerativeModel("gemini-1.5-pro")
                res = await m.generate_content_async(full_prompt)
                return res.text
        except: return f"มิติ {perspective_name} ถูกระงับตามกฎ Stop-the-Line"

async def run_truth_infrastructure(user_input, state_dict):
    # 1. รัน Survivor Engine ก่อน (Restore survival first, then restore choice)
    survivor = RealHumanSurvivorEngine()
    h_state = HumanState(**state_dict)
    survival_out = survivor.run(h_state)

    # 2. กางวงแห่งทางเลือกผ่าน AI 3 ตัวขนานกัน
    ts = TruthSystem()
    context = f"สภาวะกายภาพ: {survival_out.status}\nสิ่งที่ต้องทำทันที: {survival_out.actions}\nเหตุการณ์ที่เกิดขึ้น: {user_input}"
    
    views = await asyncio.gather(
        ts.get_view(ts.keys["gpt"], "gpt-4o", context, "เชิงโครงสร้าง (Titan)"),
        ts.get_view(ts.keys["studio"], "gemini-pro", context, "ความเป็นไปได้ (Lyla)"),
        ts.get_view(ts.keys["cloud"], "gemini-pro", context, "ความมั่นคง (Altair)")
    )
    
    return {"survival": survival_out, "perspectives": views}
