def analyze_location(lat, lng):

    zone = "unknown"

    if -10 < lat < 40 and 60 < lng < 150:
        zone = "asia"

    elif 35 < lat < 60 and -10 < lng < 40:
        zone = "europe"

    elif -40 < lat < 10 and -80 < lng < -30:
        zone = "south_america"

    return {

        "zone": zone,
        "climate_risk": "medium",
        "resource_density": "moderate"

    }
