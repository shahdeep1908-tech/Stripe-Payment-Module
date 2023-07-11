from fastapi import status
from unittest.mock import patch


class TestPaymentFailure:
    def test_customer_created_200(self, client, stripe_payload):
        with patch('stripe_webhook.webhook_router.verify_stripe_webhook_signature') as verify_stripe_webhook:
            verify_stripe_webhook.return_value = stripe_payload['customer_create']

            response = client.post('/webhook/stripe', data=stripe_payload, headers={"Stripe-Signature": "abc"})
            print("response ::: ", response)
            assert response.status_code == status.HTTP_200_OK

    def test_customer_subscription_created_200(self, client, stripe_payload):
        with patch('stripe_webhook.webhook_router.verify_stripe_webhook_signature') as verify_stripe_webhook:
            verify_stripe_webhook.return_value = stripe_payload['customer_subscription_created']

            response = client.post('/webhook/stripe', data=stripe_payload, headers={"Stripe-Signature": "abc"})
            assert response.status_code == status.HTTP_200_OK

    def test_invoice_payment_failed_200(self, client, stripe_payload):
        with patch('stripe_webhook.webhook_router.verify_stripe_webhook_signature') as verify_stripe_webhook:
            verify_stripe_webhook.return_value = stripe_payload['invoice.payment_failed']

            response = client.post('/webhook/stripe', data=stripe_payload, headers={"Stripe-Signature": "abc"})
            assert response.status_code == status.HTTP_200_OK
