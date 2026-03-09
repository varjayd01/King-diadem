# KING DIADEM Self Evolution Layer
# Allows system adaptation when new data is available

import random


def evolve_system(system_state):

    print("\nEvolution module active")

    entropy = system_state.get("entropy", 50)
    stability = system_state.get("stability", 50)

    # small adaptive correction
    adjustment = random.randint(-2, 2)

    stability += adjustment

    if stability < 0:
        stability = 0

    if stability > 100:
        stability = 100

    system_state["stability"] = stability

    print("System stability adjusted:", stability)

    return system_state
