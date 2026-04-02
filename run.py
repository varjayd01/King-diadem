from ENGINE.decision_engine import KingDiademEngine

engine = KingDiademEngine()

def ask(q):
    return input(q + ": ")

location = ask("location")
food = int(ask("food score"))
risk = int(ask("risk score"))

result = engine.run(f"{location}, food={food}, risk={risk}", mode="decision")

print(result)
