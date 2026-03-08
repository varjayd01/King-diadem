from ENGINE.decision_engine import generate_choices

# --- Language selection ---
print("Select language / เลือกภาษา")
print("1. ไทย")
print("2. English")

lang = input("Choice / ตัวเลือก: ")

if lang == "1":
    print("\nKING DIADEM ระบบช่วยตัดสินใจ")

    location = input("คุณอยู่จังหวัดอะไร: ")
    food = input("อาหารที่มีอยู่: ")
    money = input("เงินที่มี: ")
    risk = input("ความเสี่ยงตอนนี้: ")

    choices = generate_choices(location, food, money, risk)

    print("\nคำแนะนำ:\n")

    for i, c in enumerate(choices):
        print(f"{i+1}. {c}")

else:
    print("\nKING DIADEM Decision System")

    location = input("Location: ")
    food = input("Available food: ")
    money = input("Money available: ")
    risk = input("Current risk: ")

    choices = generate_choices(location, food, money, risk)

    print("\nRecommended Actions:\n")

    for i, c in enumerate(choices):
        print(f"{i+1}. {c}")
