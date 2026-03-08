import argparse
from ENGINE.decision_engine import generate_choices

def analyze():

    print("KING DIADEM Analysis")

    location = input("Location: ")
    food = input("Available food: ")
    money = input("Money available: ")
    risk = input("Risk: ")

    choices = generate_choices(location, food, money, risk)

    print("\nRecommended Actions:\n")

    for i, c in enumerate(choices):
        print(f"{i+1}. {c}")


parser = argparse.ArgumentParser()

parser.add_argument(
    "command",
    help="command to run"
)

args = parser.parse_args()

if args.command == "analyze":
    analyze()
