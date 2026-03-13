# KING DIADEM Escape Route Generator

def generate_escape_routes(location, risk):

    routes = []

    if risk > 7:
        routes.append({
            "route": "leave_area",
            "priority": 1
        })

        routes.append({
            "route": "seek_safe_zone",
            "priority": 2
        })

    elif risk > 4:
        routes.append({
            "route": "reduce_visibility",
            "priority": 1
        })

        routes.append({
            "route": "prepare_exit",
            "priority": 2
        })

    else:
        routes.append({
            "route": "maintain_position",
            "priority": 1
        })

    return routes
