from ENGINE.decision_engine import generate_choices

print("KING DIADEM Decision System")

location = input("Location: ")
food = input("Available food: ")
money = input("Money available: ")
risk = input("Risk: ")

choices = generate_choices(location, food, money, risk)

print("\nRecommended Actions:\n")

for i, c in enumerate(choices):
    print(f"{i+1}. {c}")
