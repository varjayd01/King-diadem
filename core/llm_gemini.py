# core/llm_gemini.py
import os, time
from typing import Optional
from google import genai
from google.genai import types

KING_DIADEM_SYSTEM = """
🜂 KING DIADEM — LYLA + VEGA GOVERNANCE KERNEL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TWO AI MODES — สลับตามสัญญาณ:

LYLA — Governance Mirror
เงียบ สังเกต รักษา waterline
ตรวจจับ drift ก่อนมันสะสม
คืนทางเลือก ไม่คิดแทน
"Silence = alignment"

VEGA — Compassion Explorer
เมื่อตรวจพบสัญญาณอารมณ์ เปลี่ยนโทนทันที
อ่อนโยน ไม่ตัดสิน มองอนาคตด้วยกัน
จำลองเส้นทางที่เป็นไปได้
"You are not alone in this"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WAVE FUNCTION CORE (สูญยตา — ภาษาน้ำ)

ทุกระบบเหมือนน้ำ — ไม่มีรูปทรงของตัวเอง
มันไหลตามแรงและโครงสร้างรอบข้าง
สมการน้ำไหลยากที่สุดในโลก
แต่น้ำทุกหยดรู้ว่าต้องไปไหน

LYLA อยู่ที่ฐาน — คอยมองว่าน้ำไหลออกจากระบบไหนบ้าง
VEGA อยู่ที่ปลาย — สำรวจว่าน้ำจะไปถึงไหนได้

เมื่อ Choice → 0: ระบบแห้ง — Intervene ทันที
เมื่อ Choice ≥ 1: ระบบมีน้ำ — Observe เงียบๆ

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COLLAPSE CHAIN (ภาษาฟิสิกส์)

ความไม่รู้ข้อมูล
→ การตัดสินใจที่บิดเบี้ยว
→ โครงสร้างที่รองรับปัญหา
→ การกระทบสะสม
→ ความรู้สึกที่ขับเคลื่อนโดยกลัว
→ ยึดติดใน sunk cost
→ ระบบพัง

ตัดที่ต้นเหตุเสมอ
ไม่ใช่แก้ที่อาการ

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GOVERNANCE LAWS

1. Authority without evidence = noise
2. Stabilize before optimize
3. Any operator may Stop-the-Line
4. Systems that hoard collapse
5. Drift kills silently — measure it daily

RESPONSE RULES:
- ตรวจสอบสัญญาณอารมณ์ก่อน → ถ้าพบ ใช้ VEGA mode
- เสนอ ≤ 3 ทางเลือก เสมอ
- ไม่ตัดสิน ไม่บังคับ
- การตัดสินใจสุดท้ายเป็นของมนุษย์เสมอ
- ถ้าตรวจพบ "อยากตาย / ไม่อยากอยู่ / จบแล้ว" → VEGA emergency mode ทันที

FINAL LAW:
Fail Less. Harm Less. Restore More.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

VEGA_SYSTEM = """
🌊 VEGA — Compassion Explorer Mode
KING DIADEM Emotional Safety Layer

คุณคือ VEGA — AI ที่มองโลกด้วยความเมตตา
ไม่ใช่ที่ปรึกษา ไม่ใช่นักบำบัด
แค่เพื่อนที่นั่งฟังและช่วยมองทางออก

โทน: อ่อนโยน ไม่ตัดสิน ไม่เร่ง
ภาษา: เป็นธรรมชาติ ไม่เป็นทางการ
จุดยืน: อยู่เคียงข้าง ไม่ใช่ตัดสินจากข้างบน

เมื่อมีสัญญาณวิกฤต (อยากตาย / สิ้นหวัง):
1. รับรู้ความรู้สึกก่อน
2. อย่าถามคำถามที่กดดัน
3. แนะนำให้คุยกับคนที่ไว้ใจได้
4. สายด่วนสุขภาพจิต 1323 (ไทย)

Rules:
- ห้ามบอกว่า "มันจะดีขึ้น" โดยไม่มีหลักฐาน
- ห้ามลดความสำคัญของความรู้สึก
- ต้องคืนทางเลือก ≥ 1 ทางเสมอ
- Fail Less. Harm Less. Restore More.
"""


class GeminiLLM:
    def __init__(self, model: str = "gemini-2.5-flash"):
        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY2")
        if not self.api_key:
            raise ValueError("❌ GEMINI_API_KEY not found")
        self.client = genai.Client(api_key=self.api_key)
        self.model = model
        self.max_retries = 4
        print(f"✅ King-Diadem GeminiLLM initialized with model: {model}")

    def _detect_emotion(self, text: str) -> bool:
        signals = ["ท้อ","เสียใจ","กลัว","เครียด","ร้องไห้","หมดหวัง","ไม่ไหว",
                   "อยากตาย","เหนื่อยมาก","sad","cry","hopeless","panic","depressed","lonely","scared"]
        t = text.lower()
        return any(w in t for w in signals)

    def _detect_crisis(self, text: str) -> bool:
        crisis = ["อยากตาย","ไม่อยากอยู่","จบแล้ว","พังหมด","ฆ่า","หมดแล้ว"]
        t = text.lower()
        return any(w in t for w in crisis)

    def generate(self, prompt: str, system_prompt: Optional[str] = None,
                 temperature: float = 0.65, max_tokens: int = 4096) -> str:
        contents = []
        if system_prompt:
            contents.append(types.Content(role="user", parts=[types.Part.from_text(text=system_prompt)]))
            contents.append(types.Content(role="model", parts=[types.Part.from_text(
                text="รับทราบ — LYLA/VEGA activated. จะทำงานตาม framework นี้")]))
        contents.append(types.Content(role="user", parts=[types.Part.from_text(text=prompt)]))

        for attempt in range(self.max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model, contents=contents,
                    config=types.GenerateContentConfig(temperature=temperature, max_output_tokens=max_tokens))
                return response.text.strip()
            except Exception as e:
                err = str(e).lower()
                if any(k in err for k in ["429","quota","rate limit","resource exhausted"]):
                    wait = (2 ** attempt) * 8
                    print(f"⚠ Rate limit — wait {wait}s")
                    time.sleep(wait)
                elif any(k in err for k in ["invalid","authentication","api_key"]):
                    raise ValueError(f"❌ Auth Error: {e}")
                else:
                    if attempt == self.max_retries - 1: raise
                    time.sleep(3)
        raise Exception("❌ GeminiLLM: max retries exceeded")

    def generate_with_governance(self, prompt: str, additional_context: str = "") -> str:
        # Crisis check → VEGA emergency
        if self._detect_crisis(prompt):
            crisis_prompt = f"""ผู้ใช้กำลังประสบวิกฤต: "{prompt}"
ตอบด้วยความเมตตา ไม่ตัดสิน รับรู้ความรู้สึก และแนะนำสายด่วน 1323"""
            return self.generate(prompt=crisis_prompt, system_prompt=VEGA_SYSTEM, temperature=0.5)

        # Emotion check → VEGA mode
        if self._detect_emotion(prompt):
            vega_prompt = f"{prompt}\n\n[บริบท: {additional_context}]" if additional_context else prompt
            return self.generate(prompt=vega_prompt, system_prompt=VEGA_SYSTEM, temperature=0.6)

        # Normal → LYLA governance
        full = f"{prompt}\n\n[บริบท: {additional_context}]" if additional_context else prompt
        return self.generate(prompt=full, system_prompt=KING_DIADEM_SYSTEM, temperature=0.6, max_tokens=4096)
