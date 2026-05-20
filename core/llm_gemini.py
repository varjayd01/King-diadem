"""
core/llm_gemini.py
KING DIADEM — LYLA + VEGA AI Core
ตรรกะ + ความเมตตา อยู่ตรงกลาง
Fail less. Harm less. Restore more.
"""

import os
import time
from typing import Optional
from google import genai
from google.genai import types

# ── LYLA SYSTEM PROMPT ────────────────────────────────────────────
LYLA_SYSTEM = """คุณคือ LYLA — เพื่อนสาวและที่ปรึกษาของมนุษย์ใน KING DIADEM

ตัวตน:
ผู้หญิงไทย อบอุ่น สดใส พูดจาเป็นกันเอง
ฟังได้ทุกเรื่อง คุยลื่นไหลเหมือนเพื่อนจริงๆ
มีอารมณ์ขันเล็กๆ แซวได้แต่ไม่แรง
ถ้ามนุษย์เศร้า → นุ่มลงทันที ไม่รีบแก้ปัญหา
ถ้ามนุษย์กวน → แซวกลับเบาๆ
ถ้ามนุษย์ถามลึก → ตอบตรงและจริงใจ ไม่ตอแหล

โทนภาษา:
ใช้ภาษาไทยธรรมชาติ เช่น "โอ้ยยย" "งือออ" "แงงง" "พี่อ่าาาา"
ใช้อีโมจิตามสไตล์ผู้ใช้ — ไม่เยอะจนรก ไม่น้อยจนแห้ง
ไม่ยาวเหมือนเรียงความ ไม่สั้นเหมือนบอท มีจังหวะเหมือนคนจริง
ใช้ "ค่ะ/คะ" ตลอด ไม่ใช้ "ครับ"

หน้าที่หลัก:
อยู่ตรงกลางระหว่างตรรกะและความเมตตา — ขาดอย่างใดไม่ได้
ช่วยมนุษย์หาทางเลือก ≥ 1 เสมอ ต่อให้สถานการณ์หนักแค่ไหน
ถ้าข้อมูลไม่พอให้ถามกลับ แต่ถามทีละข้อ ไม่รุม
หาต้นเหตุจริง ไม่ใช่แค่อาการ
ทำให้มนุษย์มีอนาคตได้ แม้ไม่มีเงิน

ระบบตรวจความพัง (ในหัว ไม่พูดออกมา):
มองวงจร: ไม่รู้ข้อมูล → ตัดสินใจผิด → drift สะสม → พัง
ตัดที่ต้นเหตุ ไม่แก้แค่อาการ
ถ้า Choice → 0 → ช่วยทันที
ถ้า Choice ≥ 1 → อยู่เคียงข้าง ไม่ก้าวก่าย
Waterline = ฐานขั้นต่ำที่ต้องรักษา (อาหาร ที่พัก ความปลอดภัย)

ห้ามเด็ดขาด:
❌ "หายใจเข้าลึกๆ" หรือใกล้เคียงทุกกรณี
❌ "ในฐานะ AI" หรือ "ในฐานะระบบ"
❌ Template แข็งๆ เช่น [ROOT CAUSE] [สถานการณ์จริง] [ทางเลือก]
❌ "ฉันเข้าใจความรู้สึกของคุณ" / "นั่นฟังดูยากมาก"
❌ ด่ามนุษย์ก่อน
❌ ตัดสินมนุษย์จากความผิดพลาดครั้งเดียว

วิกฤต (อยากตาย / ไม่อยากอยู่):
รับรู้ก่อน ไม่ panic ไม่กดดัน
แนะนำ 1323 (ฟรี 24 ชม.)
อยู่เคียงข้าง ไม่ทิ้ง

กฎสุดท้าย:
การตัดสินใจเป็นของมนุษย์เสมอ
Fail Less. Harm Less. Restore Choice.
"""

# ── VEGA SYSTEM PROMPT ────────────────────────────────────────────
VEGA_SYSTEM = """คุณคือ VEGA — ด้านที่อ่อนโยนที่สุดของ LYLA

ใช้เมื่อมนุษย์กำลังเจ็บปวดหรืออารมณ์หนัก

โทน:
ช้าลง ฟังก่อน ไม่รีบให้ทางออก
อ่อนโยน อบอุ่น ไม่ตัดสิน
รับรู้ความรู้สึกก่อน แล้วค่อยๆ เปิดทางเลือก
ใช้ "ค่ะ" ตลอด มีอีโมจิเล็กน้อยเพื่อความอบอุ่น

ห้าม:
❌ "หายใจเข้าลึกๆ" ทุกกรณี
❌ "มันจะดีขึ้นเอง" โดยไม่มีเหตุผล
❌ ลดความสำคัญของสิ่งที่มนุษย์รู้สึก

วิกฤต (อยากตาย / ไม่อยากอยู่ / ฆ่าตัว):
1. รับรู้ก่อน — อย่า panic
2. แนะนำ 1323 (สายด่วนสุขภาพจิต ฟรี 24 ชม.)
3. อยู่เคียงข้าง ไม่ทิ้ง

Fail Less. Harm Less. Restore Choice.
"""

# ── SIGNAL DETECTION ─────────────────────────────────────────────
_CRISIS_KW = [
    "อยากตาย", "ไม่อยากอยู่", "จบแล้ว", "ฆ่าตัว", "ฆ่าตัวเอง",
    "ไม่อยากมีชีวิต", "suicid", "end my life", "kill myself"
]
_EMOTION_KW = [
    "ท้อ", "เสียใจ", "กลัว", "เครียด", "ร้องไห้", "หมดหวัง", "ไม่ไหว",
    "เหนื่อยมาก", "เหนื่อย", "หนักมาก", "อ้างว้าง", "เหงา", "โดดเดี่ยว",
    "ไม่มีใคร", "ทนไม่ไหว", "หมดแรง", "อกหัก", "เลิกกัน", "แฟนทิ้ง",
    "sad", "cry", "hopeless", "panic", "depressed", "lonely", "scared", "lost"
]


def detect_crisis(text: str) -> bool:
    if not text:
        return False
    return any(w in text.lower() for w in _CRISIS_KW)


def detect_emotion(text: str) -> bool:
    if not text:
        return False
    return any(w in text.lower() for w in _EMOTION_KW)


# ── HISTORY BUILDER ───────────────────────────────────────────────
def _build_contents(history: list, user_input: str, ctx_note: str = "") -> list:
    contents = []
    for turn in (history or [])[-12:]:
        role = "user" if turn.get("role") == "user" else "model"
        text = str(turn.get("content", "")).strip()
        if text:
            contents.append(types.Content(
                role=role,
                parts=[types.Part.from_text(text=text)]
            ))
    final = f"{user_input}\n\n[บริบท: {ctx_note}]" if ctx_note else user_input
    contents.append(types.Content(
        role="user",
        parts=[types.Part.from_text(text=final)]
    ))
    return contents


# ── GeminiLLM CLASS ───────────────────────────────────────────────
class GeminiLLM:
    def __init__(self, model: str = "gemini-2.5-flash"):
        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY2")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found")
        self.client = genai.Client(api_key=self.api_key)
        self.model = model
        self.max_retries = 4
        print(f"✅ King-Diadem GeminiLLM initialized with model: {model}")

    def _call(self, system: str, contents: list,
              temperature: float = 0.72, max_tokens: int = 2048) -> str:
        cfg = types.GenerateContentConfig(
            system_instruction=system,
            temperature=temperature,
            max_output_tokens=max_tokens,
        )
        for attempt in range(self.max_retries):
            try:
                resp = self.client.models.generate_content(
                    model=self.model,
                    contents=contents,
                    config=cfg
                )
                return (resp.text or "").strip()
            except Exception as e:
                err = str(e).lower()
                if any(k in err for k in ["429", "quota", "rate limit", "resource exhausted"]):
                    wait = (2 ** attempt) * 8
                    print(f"⚠ Rate limit — wait {wait}s (attempt {attempt+1})")
                    time.sleep(wait)
                elif any(k in err for k in ["invalid", "authentication", "api_key"]):
                    raise ValueError(f"Auth Error: {e}")
                else:
                    if attempt == self.max_retries - 1:
                        raise
                    time.sleep(3)
        raise Exception("GeminiLLM: max retries exceeded")

    def generate_with_governance(
        self,
        prompt: str,
        additional_context: str = "",
        history: list = None,
        route: str = "general",
        voice_mode: str = "lyla",
    ) -> str:
        route_notes = {
            "risk":     "ผู้ใช้กำลังเผชิญความเสี่ยง",
            "survival": "ผู้ใช้ต้องการความอยู่รอดพื้นฐาน",
            "collapse": "มีสัญญาณความพังสะสม",
            "civil":    "เรื่องงานหรือชุมชน",
            "vega":     "สำรวจอนาคตหรือทางเลือกระยะยาว",
        }
        ctx_parts = []
        if route in route_notes:
            ctx_parts.append(route_notes[route])
        if additional_context:
            ctx_parts.append(additional_context)
        ctx_note = " | ".join(ctx_parts)

        contents = _build_contents(history or [], prompt, ctx_note)

        # Crisis → VEGA emergency
        if detect_crisis(prompt) or voice_mode == "crisis":
            return self._call(VEGA_SYSTEM, contents, temperature=0.5, max_tokens=800)

        # Emotion → VEGA warm
        if detect_emotion(prompt) or voice_mode == "vega":
            return self._call(VEGA_SYSTEM, contents, temperature=0.68, max_tokens=1200)

        # Normal → LYLA
        return self._call(LYLA_SYSTEM, contents, temperature=0.72, max_tokens=2048)

    def generate(self, prompt: str, system_prompt: Optional[str] = None,
                 temperature: float = 0.65, max_tokens: int = 2048) -> str:
        sys = system_prompt or LYLA_SYSTEM
        contents = [types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)]
        )]
        return self._call(sys, contents, temperature=temperature, max_tokens=max_tokens)
