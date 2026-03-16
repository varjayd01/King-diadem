import random

def expand_options(problem):

    base_options=[
        "observe situation",
        "reduce risk",
        "increase action",
        "collect information",
        "build alliance"
    ]

    options=[]

    for i in range(3):

        options.append({

            "strategy":random.choice(base_options),

            "risk":round(random.uniform(0.2,0.8),2),

            "confidence":round(random.uniform(0.3,0.9),2)

        })

    return options
