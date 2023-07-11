from fastapi import status
from unittest.mock import patch


class TestPaymentSuccessAfterTrial:

    def test_customer_created_200(self, client, stripe_payload):
        with patch('stripe_webhook.webhook_router.verify_stripe_webhook_signature') as verify_stripe_webhook:
            verify_stripe_webhook.return_value = stripe_payload['customer_create']
            response = client.post('/webhook/stripe', data=stripe_payload, headers={"Stripe-Signature": "abc"})
            assert response.status_code == status.HTTP_200_OK

        stripe_payload['customer_create']['id'] = "cus_2"

        with patch('stripe_webhook.webhook_router.verify_stripe_webhook_signature') as verify_stripe_webhook:
            verify_stripe_webhook.return_value = stripe_payload['customer_create']
            response = client.post('/webhook/stripe', data=stripe_payload, headers={"Stripe-Signature": "abc"})
            assert response.status_code == status.HTTP_200_OK

    def test_customer_subscription_created_200(self, client, stripe_payload):
        stripe_payload['customer_subscription_created']['status'] = "trialing"

        with patch('stripe_webhook.webhook_router.verify_stripe_webhook_signature') as verify_stripe_webhook:
            verify_stripe_webhook.return_value = stripe_payload['customer_subscription_created']
            response = client.post('/webhook/stripe', data=stripe_payload, headers={"Stripe-Signature": "abc"})
            assert response.status_code == status.HTTP_200_OK

        stripe_payload['customer_subscription_created']['customer'] = "cus_2"
        stripe_payload['customer_subscription_created']['id'] = "sub_1"

        with patch('stripe_webhook.webhook_router.verify_stripe_webhook_signature') as verify_stripe_webhook:
            verify_stripe_webhook.return_value = stripe_payload['customer_subscription_created']
            response = client.post('/webhook/stripe', data=stripe_payload, headers={"Stripe-Signature": "abc"})
            assert response.status_code == status.HTTP_200_OK

    def test_invoice_paid_200(self, client, stripe_payload):
        with patch('stripe_webhook.webhook_router.verify_stripe_webhook_signature') as verify_stripe_webhook:
            verify_stripe_webhook.return_value = stripe_payload['invoice_paid']
            response = client.post('/webhook/stripe', data=stripe_payload, headers={"Stripe-Signature": "abc"})
            assert response.status_code == status.HTTP_200_OK

    def test_customer_subscription_updated_200(self, client, stripe_payload):
        with patch('stripe_webhook.webhook_router.verify_stripe_webhook_signature') as verify_stripe_webhook:
            verify_stripe_webhook.return_value = stripe_payload['customer_subscription_updated']
            response = client.post('/webhook/stripe', data=stripe_payload, headers={"Stripe-Signature": "abc"})
            assert response.status_code == status.HTTP_200_OK
