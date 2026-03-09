# Silent Canon Kernel

def silent_canon(choice_count):

    if choice_count > 1:
        return "observe"

    if choice_count == 1:
        return "preserve_last_option"

    if choice_count == 0:
        return "emergency_intervention"
