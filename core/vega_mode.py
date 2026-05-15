# core/vega_mode.py
"""
VEGA Mode — Compassion layer ของ KING DIADEM
ไม่ใช่ template — อ่าน context จริง ตอบต่างกันทุกครั้ง
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

# keyword ที่บ่งบอก context ชัดขึ้น
_WORK_KW    = ["งาน", "บริษัท", "ลาออก", "ไล่ออก", "เจ้านาย", "เพื่อนร่วมงาน", "โปรเจกต์", "ตกงาน"]
_MONEY_KW   = ["เงิน", "หนี้", "ล้มละลาย", "ขาดทุน", "ไม่มีเงิน", "debt", "broke"]
_RELATION_KW= ["แฟน", "เลิก", "ทะเลาะ", "ครอบครัว", "พ่อ", "แม่", "เพื่อน", "ความสัมพันธ์"]
_HEALTH_KW  = ["ป่วย", "โรค", "หมอ", "รักษา", "ร่างกาย", "จิตใจ", "นอนไม่หลับ"]
_STUCK_KW   = ["ไม่รู้จะทำไง", "ตัน", "หาทางออกไม่ได้", "ไม่มีทาง", "stuck", "lost"]


def detect_crisis(text: str) -> bool:
    if not text:
        return False
    t = text.lower()
    return any(w in t for w in CRISIS_SIGNALS)


def detect_emotion(text: str) -> bool:
    if not text:
        return False
    t = text.lower()
    return any(w in t for w in EMOTION_SIGNALS)


def _detect_context(text: str) -> str:
    """อ่านว่าเรื่องนี้เกี่ยวกับอะไร"""
    t = text.lower()
    if any(w in t for w in _RELATION_KW): return "relation"
    if any(w in t for w in _WORK_KW):     return "work"
    if any(w in t for w in _MONEY_KW):    return "money"
    if any(w in t for w in _HEALTH_KW):   return "health"
    if any(w in t for w in _STUCK_KW):    return "stuck"
    return "general"


def vega_mode_hint(text: str) -> str:
    """
    คืน hint string สำหรับแนบเข้า system prompt ของ LYLA/VEGA
    บอกให้ Gemini รู้ว่า context อารมณ์คืออะไร — ไม่ใช่ template สำเร็จรูป
    """
    if detect_crisis(text):
        return (
            "[VEGA CRISIS] ผู้ใช้อาจอยู่ในภาวะวิกฤต "
            "ตอบด้วยความเมตตา รับรู้ความรู้สึกก่อน "
            "แนะนำสายด่วน 1323 อย่างนุ่มนวล "
            "ไม่ใช้คำสั่ง ไม่กดดัน"
        )

    ctx = _detect_context(text)
    hints = {
        "relation": "[VEGA] เรื่องความสัมพันธ์ — ฟังก่อน อย่าตัดสิน อย่าให้คำแนะนำเร็วเกินไป",
        "work":     "[VEGA] เรื่องงาน/อาชีพ — รับรู้ความกดดัน แล้วค่อยช่วยมองทางออก",
        "money":    "[VEGA] เรื่องเงิน/หนี้ — ไม่ตัดสิน มองว่ายังมีทางเดินไหนอีก",
        "health":   "[VEGA] เรื่องสุขภาพ — อ่อนโยน ไม่ใช้ข้อมูลแพทย์เยอะ ให้กำลังใจก่อน",
        "stuck":    "[VEGA] รู้สึกตัน — ช่วยเปิดมุมมอง ไม่รีบให้คำตอบ",
        "general":  "[VEGA] ผู้ใช้แสดงอารมณ์ — รับรู้ความรู้สึกก่อนให้ข้อมูล",
    }
    return hints.get(ctx, hints["general"])


def vega_response(user_text: str) -> dict:
    """
    ใช้สำหรับ fallback เมื่อ LLM ไม่พร้อม
    คืน dict พร้อม mode + context hint
    ไม่ใช่ template ตายตัว — ระบุ context จริง
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
