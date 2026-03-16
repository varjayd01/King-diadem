import re

LEAK_PATTERNS = [

"ไม่มีทางแล้ว",

"ชีวิตพัง",

"หมดทาง",

"เลิกกัน",

"ธุรกิจพัง",

"everything is over"

]

def detect_leak(text):

    t=text.lower()

    for p in LEAK_PATTERNS:

        if p in t:

            return True

    return False
