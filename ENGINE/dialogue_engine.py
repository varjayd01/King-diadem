import random

from WORLD_MODEL.human_behavior import detect_emotion, extract_context
from ENGINE.persona_engine import get_persona

JOKE_RESPONSES = [

    "จริงเลยพี่ 555 🤣",

    "เกือบต้องเปลี่ยนจาก Audit เป็น Cupid แล้ว",

    "รอดตายจากการเขียนจดหมายจีบสาว 100 ฉบับ",

    "ดีนะ AI ไม่ต้องแบ่ง CPU ไปคิดคำจีบสาว"
]


CLARIFY_QUESTIONS = {

    "money": [

        "เงินที่ว่าน้อย หมายถึงประมาณกี่บาทครับ",

        "งบประมาณตอนนี้ประมาณเท่าไร"

    ],

    "food": [

        "อาหารที่ว่าน้อย หมายถึงกี่มื้อครับ",

        "ตอนนี้มีอาหารพอสำหรับกี่วัน"

    ]

}


def generate_reply(text):

    emotion = detect_emotion(text)

    context = extract_context(text)

    persona = get_persona()

    if emotion == "joking":

        return random.choice(JOKE_RESPONSES)

    topic = context.get("topic")

    if topic in CLARIFY_QUESTIONS:

        return random.choice(CLARIFY_QUESTIONS[topic])

    return "ช่วยอธิบายเพิ่มอีกนิดได้ไหมครับ"
