def parse_money(value):

    text=str(value).lower()

    if "น้อย" in text:
        return 50

    if "เยอะ" in text:
        return 500

    try:
        return int(text)
    except:
        return 100
