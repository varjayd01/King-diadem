import stripe
import os

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_checkout():

    session = stripe.checkout.Session.create(

        payment_method_types=["card"],

        line_items=[{
            "price": os.getenv("STRIPE_PRICE_ID"),
            "quantity":1
        }],

        mode="payment",

        success_url="https://varjayd01.github.io/King-diadem/success.html",

        cancel_url="https://varjayd01.github.io/King-diadem/cancel.html"

    )

    return session.url
