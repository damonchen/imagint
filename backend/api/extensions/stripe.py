import stripe


def init_app(app):
    stripe.api_key = app.config["STRIPE_SECRET_KEY"]
