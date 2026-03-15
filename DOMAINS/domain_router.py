def detect_domain(text):

    text = text.lower()

    life_keywords = [
        "ชีวิต","ความรัก","ครอบครัว","ย้ายเมือง","เปลี่ยนงาน"
    ]

    business_keywords = [
        "ธุรกิจ","ลงทุน","กำไร","ขยาย","ลูกค้า","ตลาด"
    ]

    survival_keywords = [
        "เอาตัวรอด","วิกฤต","ขาดอาหาร","ภัยพิบัติ","สงคราม"
    ]

    world_keywords = [
        "โลก","เศรษฐกิจโลก","ภูมิรัฐศาสตร์","ตลาดโลก"
    ]

    for k in life_keywords:
        if k in text:
            return "life"

    for k in business_keywords:
        if k in text:
            return "business"

    for k in survival_keywords:
        if k in text:
            return "survival"

    for k in world_keywords:
        if k in text:
            return "world"

    return "general"
