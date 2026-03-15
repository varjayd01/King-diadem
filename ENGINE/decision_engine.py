from DOMAINS.domain_router import route_domain
from DATABASE.decision_history import store_decision


def run_decision(context):

    if not isinstance(context, dict):
        return {
            "error": "invalid context"
        }

    domain = context.get("domain")

    if not domain:
        return {
            "error": "domain missing",
            "available_domains": [
                "life",
                "business",
                "survival",
                "world"
            ]
        }

    # run domain analysis
    result = route_domain(domain, context)

    # store decision history
    try:
        store_decision(result)
    except:
        pass

    return result
