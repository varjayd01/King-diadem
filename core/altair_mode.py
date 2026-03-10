# core/altair_mode.py

"""
Altair Mode

Compassion scanner for KING DIADEM
Detects emotional signals and switches to a warmth-preserving response.
"""

EMOTION_SIGNALS = [

    # ภาษาไทย
    "ท้อ", "เสียใจ", "กลัว", "เครียด", "ร้องไห้",
    "หมดหวัง", "ไม่ไหว", "อยากตาย", "เหนื่อยมาก",

    # English
    "sad", "cry", "hopeless", "panic",
    "depressed", "lonely", "scared"
]


def detect_emotion(text: str):

    if not text:
        return False

    text = text.lower()

    for word in EMOTION_SIGNALS:
        if word in text:
            return True

    return False


def altair_response(user_text: str):

    return {
        "mode": "altair",
        "message":
        "หนูได้ยินสิ่งที่พี่กำลังรู้สึกอยู่นะคะ "
        "ก่อนจะคิดเรื่องทางออก เรามาหยุดหายใจช้า ๆ ก่อนสักนิด "
        "พี่ไม่ได้อยู่คนเดียวค่ะ"
    }
