from DOMAINS.domain_router import route_domain


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

    result = route_domain(domain, context)

    return result
