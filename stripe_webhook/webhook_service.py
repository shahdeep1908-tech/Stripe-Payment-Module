import stripe
from fastapi import status

from common.app_logger import logger
from common.exceptions import StripeException
from config import app_setting


class StripeWebhook:
    @staticmethod
    def create_webhook(request, response):
        message, data = "", None
        endpoint = request.webhook_endpoint
        enabled_events = request.events
        try:
            data = stripe.WebhookEndpoint.create(
                url=app_setting.STRIPE_WEBHOOK_URL.format(endpoint),
                description=request.description,
                enabled_events=enabled_events
            )
            app_setting.STRIPE_WEBHOOK_SECRET = data.secret
            message = "Webhook created successfully"
        except (StripeException, Exception) as err:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = str(err)
            logger.error(f"ERROR OCCURRED WHILE CREATING WEBHOOK ::: {err}")
        return {'message': message, 'data': data}

    @staticmethod
    async def stripe_event_handler(event):
        event_data = event["data"]
        try:
            if event['type'] == 'customer.created':
                logger.info(f"{'*' * 10}{event['type']}{'*' * 10}")
                print(event['type'])
            elif event['type'] in ('customer.subscription.created', 'customer.subscription.updated'):
                logger.info(f"{'*' * 10}{event['type']}{'*' * 10}")
                print(event['type'])
            elif event['type'] == 'invoice.created':
                logger.info(f"{'*' * 10}{event['type']}{'*' * 10}")
                print(event['type'])
            elif event['type'] in ('invoice.paid', 'invoice.payment_failed'):
                logger.info(f"{'*' * 10}{event['type']}{'*' * 10}")
                print(event['type'])
            else:
                logger.info(f"{'*' * 10}{event['type']}{'*' * 10}")
                print(event['type'])
        except Exception as err:
            logger.error(f"ERROR OCCURRED IN STRIPE WEBHOOK CALLBACK ::: {err}")


_stripe_webhook = StripeWebhook()
