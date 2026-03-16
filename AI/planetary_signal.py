import random

def planetary_signal():

    human_pressure=random.randint(20,80)

    economic_stress=random.randint(10,90)

    environment_damage=random.randint(10,70)

    conflict_risk=random.randint(5,60)

    freedom=random.randint(30,80)

    stability=round(
        (100-human_pressure+
         100-economic_stress+
         100-environment_damage+
         100-conflict_risk+
         freedom)/5
    )

    return {

        "human_pressure":human_pressure,
        "economic_stress":economic_stress,
        "environment_damage":environment_damage,
        "conflict_risk":conflict_risk,
        "freedom_signal":freedom,
        "planetary_stability":stability

    }
