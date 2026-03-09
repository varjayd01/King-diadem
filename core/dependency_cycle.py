# Dependent Cycle Engine
# System translation of causal dependency

def dependent_cycle(state):

    next_state = {}

    for key,value in state.items():

        if isinstance(value,(int,float)):

            next_state[key] = value * 0.9

        else:

            next_state[key] = value

    return next_state
