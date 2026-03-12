# KING DIADEM Path Generator

def generate_paths(lat, lng):

    routes = []

    routes.append({
        "type":"escape",
        "target":f"{lat+0.01},{lng+0.01}"
    })

    routes.append({
        "type":"resource",
        "target":f"{lat+0.02},{lng+0.02}"
    })

    return routes
