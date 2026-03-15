history = []


def store_decision(data):

    history.append(data)

    if len(history) > 1000:
        history.pop(0)


def get_history():

    return history
