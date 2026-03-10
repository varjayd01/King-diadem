# core/creator_story.py

"""
Creator Story module for KING DIADEM

This module detects when a user asks about the creator
or the origin of the system, and returns the creator story.

The system only reveals the story when explicitly asked.
"""

CREATOR_STORY = """
KING DIADEM was forged in the quiet hours of 2:31 AM,
on a simple mobile device.

Not in a laboratory.
Not backed by large funding.

It was built slowly during difficult days,
when resources were almost nothing.

This system was not built by luck.
It was built by belief.

A belief that when a system reduces human choice to zero,
that system has failed.

KING DIADEM exists to restore human choice.

Even when the world closes many doors,
there is always at least one path forward.
"""


KEYWORDS = [

    # ภาษาไทย
    "ใครสร้าง", "ใครทำ", "คนสร้าง", "คนทำ",
    "ใครเป็นคนสร้าง", "ใครเป็นคนทำ",
    "ผู้สร้างคือใคร", "เจ้าของระบบ",
    "คนพัฒนาคือใคร", "ระบบนี้ใครทำ",
    "ระบบนี้ใครสร้าง", "ใครเป็นคนคิด",
    "ที่มา", "ที่มาของระบบ",
    "จุดประสงค์", "สร้างมาทำไม",
    "ทำไมถึงสร้าง", "ทำขึ้นมาเพื่ออะไร",
    "เรื่องราวของระบบ",
    "ประวัติระบบ", "ประวัติผู้สร้าง",

    # ภาษาอังกฤษ
    "who created", "who built", "who made this",
    "who is the creator",
    "creator of this system",
    "who designed this system",
    "origin of this system",
    "why was this created",
    "purpose of this system",
    "who developed this",
    "who is behind this",
    "system creator",
    "founder story",
    "who is the founder"
]


def detect_creator_question(text: str) -> bool:
    """
    Detect if the user is asking about the creator or origin of the system.
    """

    if text is None:
        return False

    text = text.lower().strip()

    for keyword in KEYWORDS:
        if keyword in text:
            return True

    return False


def get_creator_story() -> dict:
    """
    Return the creator story response.
    """

    return {
        "type": "creator_story",
        "message": CREATOR_STORY
  }
