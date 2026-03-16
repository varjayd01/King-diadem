import random

class Simulation:

    def simulate(self,question):

        base=[

        "advance",

        "observe",

        "pivot",

        "reduce risk",

        "collect data"

        ]

        outcomes=[]

        for i in range(7):

            outcomes.append(random.choice(base))

        return outcomes
