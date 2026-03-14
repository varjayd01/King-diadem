import stripe
import os

# โหลด Stripe Secret จาก environment
stripe.api_key = os.getenv("STRIPE_SECRET")


def create_checkout(api_key: str):
    """
    Create Stripe checkout session for King Diadem credits
    """

    try:
        session = stripe.checkout.Session.create(

            payment_method_types=["card"],

            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "King Diadem Credits"
                    },
                    "unit_amount": 500
                },
                "quantity": 1
            }],

            mode="payment",

            success_url="https://king-diadem.onrender.com/success",
            cancel_url="https://king-diadem.onrender.com/cancel",

            metadata={
                "api_key": api_key
            }
        )

        return {
            "checkout_url": session.url
        }

    except Exception as e:

        return {
            "error": str(e)
        }
