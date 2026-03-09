# KING DIADEM Self Evolution Layer
# Adaptive stability correction

import random


def evolve_system(system_state):

    print("\nEvolution module active")

    entropy = system_state.get("entropy", 50)
    stability = system_state.get("stability", 50)

    adjustment = random.randint(-3, 3)

    stability = stability + adjustment

    if stability < 0:
        stability = 0

    if stability > 100:
        stability = 100

    system_state["stability"] = stability

    print("System stability adjusted:", stability)

    return system_state
