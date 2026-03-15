from DOMAINS.life_engine import analyze_life
from DOMAINS.business_engine import analyze_business
from DOMAINS.survival_engine import analyze_survival
from DOMAINS.world_engine import analyze_world


def route_domain(domain, context):

    if domain == "life":
        return analyze_life(context)

    elif domain == "business":
        return analyze_business(context)

    elif domain == "survival":
        return analyze_survival(context)

    elif domain == "world":
        return analyze_world(context)

    return {
        "error": "unknown domain",
        "available_domains": [
            "life",
            "business",
            "survival",
            "world"
        ]
    }
