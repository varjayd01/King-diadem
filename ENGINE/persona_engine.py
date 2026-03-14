DEFAULT_PERSONA = "standard"

PERSONA_STYLES = {

    "standard": {
        "tone": "friendly",
        "pronouns": "female-male",
    },

    "neutral": {
        "tone": "neutral",
        "pronouns": "gender-neutral",
    },

    "playful": {
        "tone": "humor",
        "pronouns": "adaptive",
    },

    "formal": {
        "tone": "professional",
        "pronouns": "neutral",
    }
}


def get_persona(mode=None):

    if mode is None:
        mode = DEFAULT_PERSONA

    return PERSONA_STYLES.get(mode, PERSONA_STYLES["standard"])
