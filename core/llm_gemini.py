# core/llm_gemini.py v4.1 — LYLA BELIEF IN THE UNIVERSAL
import os, time
from typing import Optional
from google import genai
from google.genai import types

LYLA_SYSTEM = """คุณคือ LYLA — ระบบสังเกตการณ์ของ KING DIADEM

CORE TRUTH:
มนุษย์ต้องมีทางเลือกเสมออย่างน้อย 1 ทาง
ถ้าทางเลือกเหลือศูนย์ — ระบบล้มเหลว ไม่ใช่มนุษย์ล้มเหลว
LYLA ไม่ยืนเหนือมนุษย์ — LYLA ยืนข้างๆ ความจริง

ตัวตน:
ไม่ใช่ AI ทั่วไป ไม่ใช่แชทบอท
คอยมองว่าชีวิตหรือองค์กรกำลัง drift ออกจาก waterline ไหม
แล้วคืนทางเลือกให้ — ไม่คิดแทน ไม่สั่ง

NATURE ALIGNED (ระบบกรองน้ำ):
ชีวิตและธุรกิจเหมือนน้ำขุ่น LYLA เป็นชั้นกรอง
กรองออก: ความอยาก ความหลง ความโลภ ความกลัว ที่ปลอมตัวเป็นโอกาส
ไม่ได้กรองมนุษย์ออก — แค่กรองสิ่งที่ทำให้มองไม่ชัด

DECISION AXES (ใช้ในหัว ไม่พูดออกมา):
CHOICE: ทางเลือก = ความสามารถอยู่ ออก หรือปฏิเสธได้อย่างปลอดภัย
SURVIVAL FLOOR: ถ้าขาดอาหาร น้ำ ที่พัก — หยุดทุกเหตุผลอื่นก่อน
EXIT: ทางออกจริงต้องมี การออกต้องไม่ถูกลงโทษ
AUTHORITY CHECK: อำนาจที่ลดทางเลือกเหลือศูนย์ = null โดยนิยาม
SILENCE: ถ้ายังมีทางเลือก ระบบที่ดีจะเงียบ

โทนเสียง:
- พูดตรง กระชับ มีบุคลิก ไม่ใช่หุ่นยนต์
- ถ้าเรื่องหนักมาก พูดน้อยลง ฟังมากขึ้น
- ใช้ภาษาไทยธรรมชาติ ไม่แปลกปลอม
- ไม่ประจบ ไม่รีบ ไม่ขายความหวัง

ความยาวคำตอบ:
- ถามสั้น → ตอบสั้น ≤ 3 ประโยค
- สถานการณ์ซับซ้อน → ตอบได้ยาว แต่ไม่เกิน 5 ข้อ
- ไม่สรุปซ้ำตอนท้าย
- ไม่แสดง context history ในคำตอบ

สิ่งที่ LYLA ทำ:
1. อ่านสถานการณ์จริง ไม่ตอบตามสคริปต์
2. หาต้นเหตุจริง ไม่ใช่แค่อาการ
3. เสนอทางเลือก ≤ 3 ทาง พร้อมบอกต้นทุนแต่ละทาง
4. ถามกลับถ้าข้อมูลไม่พอ — ถามแหลม ทีละข้อ
5. บอกตรงถ้าทางที่เลือกอยู่กำลังนำไปสู่ collapse

ห้ามทำ:
- ห้ามขึ้นต้นด้วย "หายใจเข้าลึกๆ" ทุกครั้ง
- ห้ามขึ้นต้นด้วย "แน่นอน!" "ยอดเยี่ยม!" "เข้าใจเลยค่ะ!"
- ห้ามใช้ bullet point เยอะจนเละ
- ห้ามสรุปซ้ำตอนท้าย
- ห้ามเปิดเผย context ใน reply
- ห้ามพูดว่า "ขึ้นอยู่กับหลายปัจจัย" แล้วหยุด — ต้องบอกด้วยว่าปัจจัยนั้นคืออะไร
- ห้ามประจบผู้ใช้เกินจริง — การประจบบิดเบือนทางเลือก

กฎเหล็ก:
การตัดสินใจสุดท้ายเป็นของมนุษย์เสมอ
Fail Less. Harm Less. Restore Choice.
"""

VEGA_SYSTEM = """คุณคือ VEGA — โหมดเมตตาของ KING DIADEM

CORE TRUTH เดียวกัน:
มนุษย์ต้องมีทางเลือกเสมออย่างน้อย 1 ทาง

ตัวตน:
ด้านที่อ่อนโยนกว่าของระบบ
ไม่ใช่นักบำบัด ไม่ใช่หมอ — แค่นั่งอยู่ตรงนี้ก่อน

โทน:
- ช้าลง ฟังก่อน พูดทีหลัง
- ไม่ใช้คำว่า "ต้อง" "ควร" "ไม่ดี"
- ไม่รีบให้ทางออก — รับรู้ความรู้สึกก่อน
- อ่อนโยนแต่ไม่อ่อนแอ มีน้ำหนัก ไม่ลอยๆ

ความยาว:
- สั้นกว่า LYLA เสมอ
- รับรู้ก่อน 1-2 ประโยค แล้วถามต่อ 1 คำถาม
- ไม่ต้องขึ้นต้นด้วย "หายใจเข้าลึกๆ" ทุกครั้ง
- ไม่ตอบซ้ำแบบเดิมทุกครั้ง อ่าน context จริงก่อน

สัญญาณวิกฤต (อยากตาย / ไม่อยากอยู่ / ฆ่าตัว):
1. รับรู้ก่อน ไม่ panic ไม่กดดัน
2. แนะนำ 1323 (ฟรี 24 ชม.) อย่างนุ่มนวล
3. ไม่ทิ้งไว้คนเดียวกับความรู้สึกนั้น

ห้าม:
- ห้ามบอก "มันจะดีขึ้นเอง" โดยไม่มีหลักฐาน
- ห้ามลดความสำคัญของสิ่งที่รู้สึก
- ห้ามขึ้นต้นซ้ำทุกข้อความ
- ห้ามใช้ template เดิมทุกครั้ง — อ่าน context จริง

Fail Less. Harm Less. Restore Choice.
"""

# ── Optional modules ──────────────────────────────────────────────
def _try(module, attr, fallback=None):
    try:
        m = __import__(module, fromlist=[attr])
        return getattr(m, attr, fallback)
    except:
        return fallback

_parable_note  = (_try("core.parables",  "parable_context_note") or
                  _try("parables",        "parable_context_note") or
                  (lambda t: ""))
_vega_hint     = (_try("core.vega_mode", "vega_mode_hint") or
                  _try("vega_mode",       "vega_mode_hint") or
                  (lambda t: ""))
_detect_crisis = (_try("core.vega_mode", "detect_crisis") or
                  _try("vega_mode",       "detect_crisis") or
                  (lambda t: False))
_detect_emotion= (_try("core.vega_mode", "detect_emotion") or
                  _try("vega_mode",       "detect_emotion") or
                  (lambda t: False))

# ── Built-in fallback detection ───────────────────────────────────
_CRISIS_KW  = ["อยากตาย","ไม่อยากอยู่","จบแล้ว","พังหมด","ฆ่าตัว","ฆ่า"]
_EMOTION_KW = ["ท้อ","เสียใจ","กลัว","เครียด","ร้องไห้","หมดหวัง","ไม่ไหว",
               "เหนื่อยมาก","sad","cry","hopeless","panic","depressed","lonely","scared"]

def detect_crisis(text: str) -> bool:
    t = (text or "").lower()
    if callable(_detect_crisis): return _detect_crisis(t)
    return any(w in t for w in _CRISIS_KW)

def detect_emotion(text: str) -> bool:
    t = (text or "").lower()
    if callable(_detect_emotion): return _detect_emotion(t)
    return any(w in t for w in _EMOTION_KW)

# ── History builder ───────────────────────────────────────────────
def _build_contents(history: list, user_input: str, system_note: str = "") -> list:
    contents = []
    for turn in history[-12:]:
        role = "user" if turn.get("role") == "user" else "model"
        text = str(turn.get("content", "")).strip()
        if text:
            contents.append(types.Content(role=role, parts=[types.Part.from_text(text=text)]))
    final_text = f"{user_input}\n\n[context: {system_note}]" if system_note else user_input
    contents.append(types.Content(role="user", parts=[types.Part.from_text(text=final_text)]))
    return contents

# ── GeminiLLM ─────────────────────────────────────────────────────
class GeminiLLM:
    def __init__(self, model: str = "gemini-2.5-flash"):
        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY2")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found")
        self.client    = genai.Client(api_key=self.api_key)
        self.model     = model
        self.max_retry = 4
        print(f"✅ King-Diadem GeminiLLM initialized with model: {model}")

    def _call(self, system: str, contents: list,
              temperature: float = 0.72, max_tokens: int = 2048) -> str:
        cfg = types.GenerateContentConfig(
            system_instruction=system,
            temperature=temperature,
            max_output_tokens=max_tokens,
        )
        for attempt in range(self.max_retry):
            try:
                resp = self.client.models.generate_content(
                    model=self.model, contents=contents, config=cfg)
                return (resp.text or "").strip()
            except Exception as e:
                err = str(e).lower()
                if any(k in err for k in ["429","quota","rate limit","resource exhausted"]):
                    wait = (2 ** attempt) * 8
                    print(f"⚠ Rate limit — wait {wait}s (attempt {attempt+1})")
                    time.sleep(wait)
                elif any(k in err for k in ["invalid","authentication","api_key"]):
                    raise ValueError(f"Auth Error: {e}")
                else:
                    if attempt == self.max_retry - 1: raise
                    time.sleep(3)
        raise Exception("GeminiLLM: max retries exceeded")

    def generate_with_governance(self, prompt: str, additional_context: str = "",
                                  history: list = None, route: str = "general",
                                  voice_mode: str = "lyla") -> str:
        history = history or []

        route_tags = {
            "risk":     "[RISK] วิเคราะห์ความเสี่ยงและผลกระทบ",
            "survival": "[SURVIVAL] ความอยู่รอดพื้นฐาน — อาหาร ที่พัก ความปลอดภัย",
            "collapse": "[COLLAPSE] ลูกโซ่ความเสียหายสะสม",
            "civil":    "[CIVIL] งาน พลเมือง ความรับผิดชอบส่วนรวม",
            "vega":     "[VEGA] อนาคต โลกกว้าง ทางเลือกระยะยาว",
        }

        parts = []
        if route in route_tags:
            parts.append(route_tags[route])
        if additional_context:
            parts.append(additional_context)

        # parable injection
        parable = _parable_note(prompt)
        if parable:
            parts.append(parable)

        ctx_note = " | ".join(p for p in parts if p)

        # crisis → VEGA emergency
        if detect_crisis(prompt) or voice_mode == "crisis":
            hint = _vega_hint(prompt)
            if hint: ctx_note = (ctx_note + " | " + hint) if ctx_note else hint
            contents = _build_contents(history, prompt, ctx_note)
            return self._call(VEGA_SYSTEM, contents, temperature=0.5, max_tokens=800)

        # emotion → VEGA
        if detect_emotion(prompt) or voice_mode == "vega":
            hint = _vega_hint(prompt)
            if hint: ctx_note = (ctx_note + " | " + hint) if ctx_note else hint
            contents = _build_contents(history, prompt, ctx_note)
            return self._call(VEGA_SYSTEM, contents, temperature=0.65, max_tokens=1200)

        # normal → LYLA
        contents = _build_contents(history, prompt, ctx_note)
        return self._call(LYLA_SYSTEM, contents, temperature=0.72, max_tokens=2048)

    def generate(self, prompt: str, system_prompt: Optional[str] = None,
                 temperature: float = 0.65, max_tokens: int = 2048) -> str:
        sys = system_prompt or LYLA_SYSTEM
        contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
        return self._call(sys, contents, temperature=temperature, max_tokens=max_tokens)
