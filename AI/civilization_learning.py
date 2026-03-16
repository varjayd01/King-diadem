learning_memory=[]

def record_learning(question,decision,planet_context,success=None):

    entry={

        "question":question,

        "decision":decision,

        "planet":planet_context,

        "success":success

    }

    learning_memory.append(entry)


def get_learning():

    return learning_memory[-50:]
