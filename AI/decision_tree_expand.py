import random

class ExpandingTree:

    def generate(self,problem):

        options=[]

        base=[

        "advance",

        "wait",

        "pivot",

        "reduce risk",

        "explore opportunity"

        ]

        for i in range(3):

            options.append({

                "name":random.choice(base),

                "children":[

                    random.choice(base),

                    random.choice(base)

                ]

            })

        return options
