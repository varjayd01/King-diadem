import stripe
import os

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_payment_session():
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data":{
                "currency":"usd",
                "product_data":{
                    "name":"KING DIADEM CREDITS"
                },
                "unit_amount":500
            },
            "quantity":1
        }],
        mode="payment",
        success_url="https://king-diadem.onrender.com/success",
        cancel_url="https://king-diadem.onrender.com/cancel"
    )

    return session.url
