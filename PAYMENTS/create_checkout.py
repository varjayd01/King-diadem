import stripe
import os

stripe.api_key=os.getenv("STRIPE_SECRET")

def create_checkout(api_key):

    session=stripe.checkout.Session.create(

        payment_method_types=["card"],

        line_items=[{

            "price_data":{

                "currency":"usd",

                "product_data":{
                    "name":"King Diadem Credits"
                },

                "unit_amount":500

            },

            "quantity":1
        }],

        mode="payment",

        success_url="https://king-diadem.onrender.com",

        cancel_url="https://king-diadem.onrender.com",

        metadata={
            "api_key":api_key
        }

    )

    return session.url
