import random

from AI.decision_memory import store_decision


def process_decision(question):

    options=[

        "gather more information",
        "take cautious action",
        "wait and observe",
        "seek collaboration"

    ]

    random.shuffle(options)

    store_decision(question,options)

    return options
