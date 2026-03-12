# KING DIADEM Escape Route Generator

from ENGINE.map_bridge import open_google_maps

def generate_escape_route(lat, lng):

    safe_point = f"{lat+0.01},{lng+0.01}"

    route = f"https://www.google.com/maps/dir/{lat},{lng}/{safe_point}"

    return route
