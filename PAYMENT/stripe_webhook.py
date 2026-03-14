import stripe
import os
from DATABASE.credit_store import add_credits

stripe.api_key = os.getenv("STRIPE_SECRET")

processed_events = set()

def handle_webhook(event):

    event_id = event["id"]

    # กัน webhook ซ้ำ
    if event_id in processed_events:
        return "duplicate"

    processed_events.add(event_id)

    if event["type"] == "checkout.session.completed":

        session = event["data"]["object"]

        api_key = session["metadata"]["api_key"]

        amount = session["amount_total"] / 100

        credits = int(amount)

        add_credits(api_key, credits)

    return "ok"
