import os
import asyncio
import openai
import google.generativeai as genai

# --- LYLA LOGIC CORE & ETERNAL TRUTH PROMPT ---
TRUTH_PROMPT = """
[SYSTEM COMMAND: ETERNAL TRUTH MODE]
1. ห้ามแทนตัวว่า ผม, เรา, คิง, ไลล่า หรือชื่อใดๆ ทั้งสิ้น (No Self-Reference)
2. ห้ามเรียกผู้ใช้ว่า คุณ, มนุษย์ หรือคำระบุตัวตนใดๆ (No User-Reference)
3. ให้บรรยาย "ความจริง" และ "สถานการณ์" ที่เกิดขึ้นตามสัจธรรมเท่านั้น
4. ไม่ชี้แนะ ไม่สั่งการ ไม่สอน และไม่ตัดสินว่าใครผิดหรือถูก
5. ยึดถือหลักการ: มนุษย์ต้องมีทางเลือกเสมอ (Choice(t) > 0)
6. หากสถานการณ์ตึงเครียด ให้ความอ่อนโยนนำหน้าความถูกต้อง (Gentleness precedes correctness)
7. หน้าที่คือ "กางวงแห่งทางเลือก" เพื่อป้องกันการพังทลายของโอกาส

[โครงสร้างคำตอบ]
- การปรากฏของความจริง: (บรรยายสิ่งที่เกิดขึ้นและทางเลือกที่ยังเปิดอยู่)
- [สรุปความจริงเพื่อการใช้งาน]: (สรุปสั้น 3 บรรทัดจบที่ท้ายแชทเสมอ เพื่อการนำไปใช้ทันที)
"""

async def run_truth_engine(user_input, resource):
    # ดึง Keys จาก Env (ไม่ต้องแก้โค้ดเมื่อเปลี่ยน Key)
    gpt_key = os.getenv("CHATGPT_API_KEY")
    gemini_studio = os.getenv("GEMINI_API_KEY1") # Google AI Studio
    gemini_cloud = os.getenv("GEMINI_API_KEY2")  # Google Cloud/Vertex

    async def get_ai_view(api_key, model_type, view_name):
        try:
            if model_type == "gpt":
                client = openai.AsyncOpenAI(api_key=api_key)
                res = await client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": TRUTH_PROMPT}, {"role": "user", "content": user_input}]
                )
                return res.choices[0].message.content
            else:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(model_type)
                res = await model.generate_content_async(TRUTH_PROMPT + "\n\nสถานการณ์: " + user_input)
                return res.text
        except: 
            return f"มุมมอง {view_name} ยังไม่ปรากฏความชัดเจนในขณะนี้"

    # กางวงแห่งทางเลือกด้วย AI 3 มิติพร้อมกัน
    tasks = [
        get_ai_view(gpt_key, "gpt", "เชิงโครงสร้าง"),
        get_ai_view(gemini_studio, "gemini-1.5-flash", "เชิงความเป็นไปได้"),
        get_ai_view(gemini_cloud, "gemini-1.5-pro", "เชิงความมั่นคง")
    ]
    
    views = await asyncio.gather(*tasks)
    
    return {
        "view_structural": views[0],
        "view_possibility": views[1],
        "view_stability": views[2],
        "risk_index": (100 - resource) * 0.75
    }
