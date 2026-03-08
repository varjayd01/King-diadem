# KING DIADEM Decision Engine Prototype

def generate_choices(location, food, money, risk):

    choices = []

    # Resource balancing
    if "food shortage" in risk:
        choices.append("Reduce food consumption cycle and prioritize high nutrition food")

    # Local sourcing
    choices.append("Search for local food sources or community sharing")

    # Micro production
    choices.append("Start micro food production (home garden or simple crops)")

    # Risk reduction
    choices.append("Reduce unnecessary movement and maintain health stability")

    return choices


def main():

    print("KING DIADEM Survival Decision Engine\n")

    location = input("Location: ")
    food = input("Available food: ")
    money = input("Money available: ")
    risk = input("Current risk: ")

    choices = generate_choices(location, food, money, risk)

    print("\nRecommended Survival Choices:\n")

    for i, choice in enumerate(choices):
        print(f"{i+1}. {choice}")


if __name__ == "__main__":
    main()
