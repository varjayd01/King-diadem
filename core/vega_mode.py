"""
core/vega_mode.py
VEGA Mode — Compassion layer ของ KING DIADEM
ตรวจ context จริง คืน signal ให้ LYLA/Gemini
ไม่ใช่ template — ไม่ใช้ภาษา therapist
Fail less. Harm less. Restore more.
"""

# ── Signal lists ──────────────────────────────────────────────────

CRISIS_SIGNALS = [
    "อยากตาย", "ไม่อยากอยู่", "จบแล้ว", "ฆ่าตัว", "ฆ่าตัวเอง",
    "ไม่อยากมีชีวิต", "หมดแล้วจริงๆ", "suicid", "end my life", "kill myself"
]

EMOTION_SIGNALS = [
    "ท้อ", "เสียใจ", "กลัว", "เครียด", "ร้องไห้", "หมดหวัง", "ไม่ไหว",
    "เหนื่อยมาก", "เหนื่อย", "หนักมาก", "อ้างว้าง", "เหงา", "โดดเดี่ยว",
    "ไม่มีใคร", "ไม่รู้จะทำยังไง", "ทนไม่ไหว", "หมดแรง",
    "sad", "cry", "hopeless", "panic", "depressed", "lonely", "scared", "lost"
]

_WORK_KW     = ["งาน", "บริษัท", "ลาออก", "ไล่ออก", "เจ้านาย", "เพื่อนร่วมงาน", "โปรเจกต์", "ตกงาน"]
_MONEY_KW    = ["เงิน", "หนี้", "ล้มละลาย", "ขาดทุน", "ไม่มีเงิน", "debt", "broke"]
_RELATION_KW = ["แฟน", "เลิก", "ทะเลาะ", "ครอบครัว", "พ่อ", "แม่", "เพื่อน", "ความสัมพันธ์"]
_HEALTH_KW   = ["ป่วย", "โรค", "หมอ", "รักษา", "ร่างกาย", "จิตใจ", "นอนไม่หลับ"]
_STUCK_KW    = ["ไม่รู้จะทำไง", "ตัน", "หาทางออกไม่ได้", "ไม่มีทาง", "stuck", "lost"]


def detect_crisis(text: str) -> bool:
    if not text:
        return False
    return any(w in text.lower() for w in CRISIS_SIGNALS)


def detect_emotion(text: str) -> bool:
    if not text:
        return False
    return any(w in text.lower() for w in EMOTION_SIGNALS)


def _detect_context(text: str) -> str:
    t = text.lower()
    if any(w in t for w in _RELATION_KW): return "relation"
    if any(w in t for w in _WORK_KW):     return "work"
    if any(w in t for w in _MONEY_KW):    return "money"
    if any(w in t for w in _HEALTH_KW):   return "health"
    if any(w in t for w in _STUCK_KW):    return "stuck"
    return "general"


def vega_mode_hint(text: str) -> str:
    """
    คืน hint string สำหรับแนบเข้า system prompt
    บอก Gemini ว่า context คืออะไร
    ไม่ใช่ template — ไม่มีประโยค therapist
    """
    if detect_crisis(text):
        return (
            "[VEGA CRISIS] ผู้ใช้อาจอยู่ในภาวะวิกฤต "
            "ระบุทางออกที่มีอยู่จริงก่อน "
            "แนะนำสายด่วน 1323 "
            "ไม่ใช้คำสั่ง ไม่กดดัน "
            "คืนทางเลือก ≥ 1 เสมอ"
        )

    ctx = _detect_context(text)
    hints = {
        "relation": "[VEGA] relation — รับรู้ก่อน อย่าตัดสิน คืนทางเลือก",
        "work":     "[VEGA] work — ระบุข้อจำกัดจริง แล้วมองทางออกที่เป็นไปได้",
        "money":    "[VEGA] money — ระบุทรัพยากรที่มีจริง ไม่ตัดสิน",
        "health":   "[VEGA] health — อ่อนโยน ไม่วินิจฉัย คืนทางเลือก",
        "stuck":    "[VEGA] stuck — เปิดมุมมอง ไม่รีบให้คำตอบ",
        "general":  "[VEGA] emotion detected — รับรู้ก่อน แล้วคืนทางเลือก",
    }
    return hints.get(ctx, hints["general"])


def vega_response(user_text: str) -> dict:
    """
    Fallback เมื่อ LLM ไม่พร้อม
    คืน signal + choices — ไม่ใช่ข้อความสำเร็จรูป
    """
    if detect_crisis(user_text):
        return {
            "mode":    "vega_crisis",
            "context": "crisis",
            "hint":    vega_mode_hint(user_text),
            "choices": ["โทร 1323", "คุยกับคนที่ไว้ใจได้", "เล่าต่อได้เลย"],
        }

    ctx = _detect_context(user_text)
    return {
        "mode":    "vega",
        "context": ctx,
        "hint":    vega_mode_hint(user_text),
        "choices": ["เล่าต่อ", "ขอทางออก", "แค่อยากระบาย"],
    }
