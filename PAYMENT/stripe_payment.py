import stripe
import os

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_payment_session():

    session = stripe.checkout.Session.create(

        payment_method_types=["card"],

        line_items=[{
            "price": os.getenv("STRIPE_PRICE_ID"),
            "quantity": 1
        }],

        mode="payment",

        success_url="https://king-diadem.onrender.com/success",
        cancel_url="https://king-diadem.onrender.com/cancel",

        metadata={
            "api_key": "KING-001"
        }

    )

    return session.url
