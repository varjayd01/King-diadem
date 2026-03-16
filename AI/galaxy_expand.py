import random

class GalaxyExpansion:

    def expand(self,option):

        new=[]

        base=[

        "increase investment",
        "reduce exposure",
        "test prototype",
        "collect market signal",
        "build alliance"

        ]

        for i in range(random.randint(2,4)):

            new.append(random.choice(base))

        return new
