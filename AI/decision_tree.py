import random

class DecisionTree:

    def generate_paths(self, problem):

        base_paths = [

            "advance strategy",
            "wait and observe",
            "reduce exposure",
            "pivot direction",
            "collect more data"

        ]

        paths = []

        for i in range(3):

            paths.append({

                "option": f"Path {i+1}",

                "strategy": random.choice(base_paths),

                "risk": round(random.uniform(0.1,0.9),2),

                "confidence": round(random.uniform(0.2,0.95),2)

            })

        return {

            "problem": problem,

            "paths": paths

        }
