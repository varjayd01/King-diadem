decision_memory=[]


def store_decision(question,options):

    node={
        "question":question,
        "options":options
    }

    decision_memory.append(node)


def get_memory():

    return decision_memory[-50:]
