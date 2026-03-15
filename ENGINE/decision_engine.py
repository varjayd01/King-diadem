from DOMAINS.domain_router import route_domain
from DATABASE.decision_history import save_decision


def run_decision(context):

    # ---------- VALIDATION ----------

    if not isinstance(context, dict):

        return {
            "error": "invalid context"
        }


    # ---------- DOMAIN CHECK ----------

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


    # ---------- ROUTE DOMAIN ----------

    try:

        result = route_domain(domain, context)

    except Exception as e:

        return {

            "error": "decision engine failure",

            "detail": str(e)
        }


    # ---------- STORE DECISION ----------

    try:

        save_decision(result)

    except Exception:

        pass


    # ---------- FINAL RESULT ----------

    return result
