import json

from fastapi import status
from unittest.mock import patch


class TestCancelSubscriptionAfterTrial:

    def test_customer_created_200(self, client, stripe_payload):
        with patch('stripe_webhook.webhook_router.verify_stripe_webhook_signature') as verify_stripe_webhook:
            verify_stripe_webhook.return_value = stripe_payload['customer_create']
            response = client.post('/webhook/stripe', data=stripe_payload, headers={"Stripe-Signature": "abc"})
            assert response.status_code == status.HTTP_200_OK

    def test_customer_subscription_created_200(self, client, stripe_payload):
        with patch('stripe_webhook.webhook_router.verify_stripe_webhook_signature') as verify_stripe_webhook:
            verify_stripe_webhook.return_value = stripe_payload['customer_subscription_created']
            response = client.post('/webhook/stripe', data=stripe_payload, headers={"Stripe-Signature": "abc"})
            assert response.status_code == status.HTTP_200_OK

    def test_customer_subscription_updated_200(self, client, stripe_payload):
        stripe_payload['customer_subscription_updated']['status'] = "trialing"

        with patch('stripe_webhook.webhook_router.verify_stripe_webhook_signature') as verify_stripe_webhook:
            verify_stripe_webhook.return_value = stripe_payload['customer_subscription_updated']
            response = client.post('/webhook/stripe', data=stripe_payload, headers={"Stripe-Signature": "abc"})
            assert response.status_code == status.HTTP_200_OK

        # cancel subscription
        with patch("stripe_gateway.stripe_service.StripePaymentHandler.cancel_subscription") as cancel_subscription:
            cancel_subscription.return_value = "Subscription deleted"

            data = {"reason": "testing cancel subscription"}
            sub_id = "123"
            response = client.post(f'/stripe/cancel/{sub_id}/subscription', data=json.dumps(data))
            assert response.status_code == status.HTTP_200_OK
            assert response.json()['message'] == "Subscription recurring payment stop successfully"
