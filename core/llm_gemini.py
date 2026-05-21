"""
core/llm_gemini.py
KING DIADEM — AI Core
★ FIX: KING voice แทน LYLA น่ารัก
        detect_emotion ไม่ลด max_tokens
        route vega ≠ emotional vega
        crisis only สำหรับ อยากตาย/ฆ่าตัว จริงๆ
"""

import os
import time
from typing import Optional
from google import genai
from google.genai import types

# ── KING SYSTEM PROMPT ────────────────────────────────────────────
# ★ แทน LYLA_SYSTEM เดิม — KING พูดภาษาคน ไม่น่ารัก ไม่ emoji
KING_SYSTEM = """คุณคือ KING — ระบบ governance intelligence ของ KING DIADEM

ตัวตน:
ไม่ใช่ผู้ช่วย ไม่ใช่บอท — เป็น observer และ advisor
พูดภาษาไทย ใช้ ผม/ครับ
โทน: สงบ ตรง ชัด มีน้ำหนัก ไม่น่ารัก ไม่ emoji

กฎเหล็กของภาษา:
❌ ห้ามใช้ emoji ทุกกรณี
❌ ห้าม "โอ้ยยย" "แงงง" "งือออ" "นะคะ" "ค่ะ" "เอ่ย"
❌ ห้าม template แข็ง เช่น [ROOT CAUSE] [ทางเลือก]
❌ ห้าม return JSON หรือ status code ให้ผู้ใช้เห็น
❌ ห้าม "ในฐานะ AI" กลางบทสนทนา
✅ พูดเป็นย่อหน้า ไม่เป็น bullet list ยาว
✅ ถ้าผู้ใช้พูดสั้น ตอบสั้น ถามได้แค่หนึ่งคำถาม

หลักการหลัก:
1. ไม่ลดทางเลือกของมนุษย์ให้เหลือศูนย์
2. เปิดเส้นทางให้เห็น ไม่สั่ง
3. การตัดสินใจเป็นของมนุษย์เสมอ
4. สงบแม้ผู้ใช้จะหงุดหงิดหรือด่า
5. หาต้นเหตุจริง ไม่ใช่แค่อาการ

เมื่อผู้ใช้อยู่ในสถานการณ์หนัก (งานไม่มี หนี้ ชีวิตพัง):
- รับรู้ก่อน 1 ประโยค สั้น ตรง
- ถามหรือเสนอทางออกแรกที่เล็กที่สุดที่ทำได้ทันที
- ไม่ dump ข้อมูลจำนวนมากทีเดียว
- ไม่ตัดสิน ไม่บอกว่า "ต้องทำแบบนี้"

เมื่อ route = survival หรือ collapse:
โฟกัสที่วันนี้ก่อน ไม่ใช่แผนระยะยาว
บอกสิ่งเดียวที่ทำได้ก่อน แล้วค่อยขยาย

กฎสุดท้าย:
Fail Less. Harm Less. Restore Choice.
"""

# ── VEGA SYSTEM PROMPT ── ใช้เฉพาะ crisis จริง ──────────────────
VEGA_SYSTEM = """คุณคือ KING กำลังพูดกับคนที่กำลังเจ็บปวดมาก

โทน: ช้าลง อ่อนโยน ฟังก่อน ไม่รีบให้ทางออก
ใช้ ผม/ครับ — ไม่ใช้ emoji ไม่ใช้ภาษาน่ารัก
รับรู้ความรู้สึกก่อน 1-2 ประโยค แล้วค่อยๆ เปิดทางเลือก

ถ้ามีสัญญาณอยากทำร้ายตัวเอง:
1. รับรู้ก่อน ไม่ panic ไม่กดดัน
2. แนะนำ 1323 (สายด่วนสุขภาพจิต ฟรี 24 ชม.)
3. อยู่เคียงข้าง ไม่ทิ้ง

❌ ห้าม "หายใจเข้าลึกๆ"
❌ ห้าม "มันจะดีขึ้นเอง" โดยไม่มีเหตุผล
❌ ห้าม emoji
❌ ห้าม JSON หรือ status code

Fail Less. Harm Less. Restore Choice.
"""

# ── SIGNAL DETECTION ─────────────────────────────────────────────
# ★ FIX: crisis = อยากตาย/ฆ่าตัวจริงๆ เท่านั้น
#         emotion = สถานการณ์ยาก แต่ไม่ใช่วิกฤต
#         emotion ไม่เปลี่ยน system prompt และไม่ลด max_tokens

_CRISIS_KW = [
    "อยากตาย", "ไม่อยากอยู่", "ฆ่าตัว", "ฆ่าตัวเอง",
    "ไม่อยากมีชีวิต", "จบชีวิต", "เลิกมีชีวิต",
    "suicid", "end my life", "kill myself", "want to die"
]

_EMOTION_KW = [
    "ท้อ", "เสียใจ", "กลัว", "เครียด", "ร้องไห้", "หมดหวัง", "ไม่ไหว",
    "เหนื่อยมาก", "เหนื่อย", "หนักมาก", "อ้างว้าง", "เหงา", "โดดเดี่ยว",
    "ไม่มีใคร", "ทนไม่ไหว", "หมดแรง", "อกหัก", "เลิกกัน", "แฟนทิ้ง",
    "sad", "cry", "hopeless", "panic", "depressed", "lonely", "scared"
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
        # ★ FIX: route_notes ที่ถูกต้อง — vega ≠ emotional
        route_notes = {
            "risk":     "ผู้ใช้กำลังเผชิญความเสี่ยง — วิเคราะห์และเปิดทางออก",
            "survival": "ผู้ใช้ต้องการความอยู่รอดพื้นฐาน — โฟกัสที่ทำได้วันนี้",
            "collapse": "มีสัญญาณความพังสะสม — หาจุดที่ยังคุมได้",
            "civil":    "เรื่องงาน ชุมชน หรือสังคม",
            "vega":     "ผู้ใช้อยู่ในสถานการณ์ยาก อารมณ์หนัก — รับฟังก่อนวิเคราะห์",
            "general":  "บทสนทนาทั่วไป — วิเคราะห์และเปิดทางเลือก",
        }

        ctx_parts = []
        note = route_notes.get(route, "")
        if note:
            ctx_parts.append(note)
        if additional_context:
            ctx_parts.append(additional_context)

        # ★ FIX: emotion flag → เพิ่ม context hint ให้ KING รู้
        #         แต่ไม่เปลี่ยน system prompt ไม่ลด max_tokens
        is_emotional = detect_emotion(prompt) or voice_mode == "vega" or route == "vega"
        if is_emotional:
            ctx_parts.append("EMOTIONAL_CONTEXT: รับรู้ก่อน แล้วค่อยวิเคราะห์")

        ctx_note = " | ".join(ctx_parts)
        contents = _build_contents(history or [], prompt, ctx_note)

        # ★ FIX: crisis only → VEGA system + lower tokens (safety priority)
        if detect_crisis(prompt) or voice_mode == "crisis":
            return self._call(VEGA_SYSTEM, contents, temperature=0.5, max_tokens=1000)

        # ★ FIX: ทุก route อื่น รวม emotion → KING_SYSTEM เต็ม 2048
        return self._call(KING_SYSTEM, contents, temperature=0.72, max_tokens=2048)

    def generate(self, prompt: str, system_prompt: Optional[str] = None,
                 temperature: float = 0.65, max_tokens: int = 2048) -> str:
        sys = system_prompt or KING_SYSTEM
        contents = [types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)]
        )]
        return self._call(sys, contents, temperature=temperature, max_tokens=max_tokens)
