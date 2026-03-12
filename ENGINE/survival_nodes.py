# KING DIADEM Survival Node Scanner

from ENGINE.map_bridge import open_google_maps

def find_survival_nodes(lat, lng):

    nodes = {
        "food": open_google_maps(lat, lng),
        "hospital": open_google_maps(lat, lng),
        "water": open_google_maps(lat, lng)
    }

    return nodes
