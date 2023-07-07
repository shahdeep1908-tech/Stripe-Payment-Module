import stripe
from config import app_setting


def verify_stripe_webhook_signature(payload, stripe_signature):
    return stripe.Webhook.construct_event(payload=payload, sig_header=stripe_signature,
                                          secret=app_setting.STRIPE_WEBHOOK_SECRET)
