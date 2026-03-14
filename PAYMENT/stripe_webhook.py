import stripe
import os
from DATABASE.credit_store import add_credits

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

processed_events = set()

def handle_webhook(payload, sig_header):

    event = stripe.Webhook.construct_event(
        payload,
        sig_header,
        WEBHOOK_SECRET
    )

    event_id = event["id"]

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
