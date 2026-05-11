# core/vega_mode.py
"""
VEGA Mode — Compassion scanner for KING DIADEM
Detects emotional signals and switches to warmth-preserving response.
"""

EMOTION_SIGNALS = [
    "ท้อ","เสียใจ","กลัว","เครียด","ร้องไห้","หมดหวัง","ไม่ไหว",
    "อยากตาย","เหนื่อยมาก","sad","cry","hopeless","panic","depressed","lonely","scared"
]

CRISIS_SIGNALS = ["อยากตาย","ไม่อยากอยู่","จบแล้ว","พังหมด","ฆ่า"]

def detect_emotion(text: str) -> bool:
    if not text:
        return False
    t = text.lower()
    return any(w in t for w in EMOTION_SIGNALS)

def detect_crisis(text: str) -> bool:
    if not text:
        return False
    t = text.lower()
    return any(w in t for w in CRISIS_SIGNALS)

def vega_response(user_text: str) -> dict:
    if detect_crisis(user_text):
        return {
            "mode": "vega_crisis",
            "message": (
                "หนูได้ยินสิ่งที่พี่รู้สึกอยู่นะคะ\n\n"
                "ตอนนี้ขอให้หยุดหายใจช้าๆ ก่อนสักครู่\n"
                "พี่ไม่ได้อยู่คนเดียวในความรู้สึกนี้\n\n"
                "ถ้าต้องการคุยกับผู้เชี่ยวชาญตอนนี้เลย:\n"
                "📞 สายด่วนสุขภาพจิต 1323 (ฟรี 24 ชม.)"
            ),
            "choices": ["โทร 1323 ตอนนี้", "คุยกับคนที่ไว้ใจได้", "บอกหนูต่อว่าเกิดอะไรขึ้น"]
        }

    return {
        "mode": "vega",
        "message": (
            "หนูได้ยินนะคะ\n\n"
            "ก่อนจะคิดเรื่องทางออก — พี่รู้สึกยังไงอยู่ตอนนี้คะ?\n"
            "ไม่ต้องรีบ ค่อยๆ เล่าได้เลย"
        ),
        "choices": ["เล่าให้ฟังต่อ", "ขอทางออกก่อน", "แค่อยากระบาย"]
    }
