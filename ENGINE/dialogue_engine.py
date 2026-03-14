import random
from WORLD_MODEL.human_behavior import detect_emotion

JOKE_RESPONSES = [
    "จริงเลยพี่ 555 🤣",
    "เกือบต้องเปลี่ยนระบบเป็น Cupid แล้วนะเนี่ย",
    "ระวังนะ เดี๋ยว AI ต้องเขียนจดหมายจีบแทน",
]

CLARIFY_QUESTIONS = {
    "money": [
        "เงินที่ว่าน้อย หมายถึงประมาณกี่บาทครับ",
        "งบประมาณตอนนี้ประมาณเท่าไร",
    ],
    "food": [
        "อาหารที่ว่าน้อย หมายถึงกี่มื้อครับ",
        "ตอนนี้มีอาหารพอสำหรับกี่วัน",
    ]
}


def generate_reply(text, context):

    emotion = detect_emotion(text)

    if emotion == "joking":
        return random.choice(JOKE_RESPONSES)

    topic = context.get("topic")

    if topic in CLARIFY_QUESTIONS:
        return random.choice(CLARIFY_QUESTIONS[topic])

    return "ช่วยอธิบายเพิ่มอีกนิดได้ไหมครับ"
