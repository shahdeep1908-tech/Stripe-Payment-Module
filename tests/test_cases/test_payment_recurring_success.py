import time
from fastapi import status
from unittest.mock import patch
from datetime import datetime


class TestRecurringPaymentSuccess:

    def test_customer_created_200(self, client, stripe_payload):
        with patch('stripe_webhook.webhook_router.verify_stripe_webhook_signature') as verify_stripe_webhook:
            verify_stripe_webhook.return_value = stripe_payload['customer_create']
            response = client.post('/webhook/stripe', data=stripe_payload, headers={"Stripe-Signature": "abc"})
            assert response.status_code == status.HTTP_200_OK

    def test_customer_subscription_created_200(self, client, stripe_payload):
        now = datetime.now()
        unix_timestamp = time.mktime(now.timetuple())

        stripe_payload['customer_subscription_created']['current_period_end'] = unix_timestamp

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
        now = datetime.now()
        unix_timestamp = time.mktime(now.timetuple())

        stripe_payload['customer_subscription_updated']['current_period_end'] = unix_timestamp

        with patch('stripe_webhook.webhook_router.verify_stripe_webhook_signature') as verify_stripe_webhook:
            verify_stripe_webhook.return_value = stripe_payload['customer_subscription_updated']
            response = client.post('/webhook/stripe', data=stripe_payload, headers={"Stripe-Signature": "abc"})
            assert response.status_code == status.HTTP_200_OK

        # recurring payment success events
        stripe_payload['invoice_paid']['payment_intent'] = "pi_1"
        with patch('stripe_webhook.webhook_router.verify_stripe_webhook_signature') as verify_stripe_webhook:
            verify_stripe_webhook.return_value = stripe_payload['invoice_paid']
            response = client.post('/webhook/stripe', data=stripe_payload, headers={"Stripe-Signature": "abc"})
            assert response.status_code == status.HTTP_200_OK

        stripe_payload['customer_subscription_updated']['current_period_end'] = unix_timestamp
        with patch('stripe_webhook.webhook_router.verify_stripe_webhook_signature') as verify_stripe_webhook:
            verify_stripe_webhook.return_value = stripe_payload['customer_subscription_updated']
            response = client.post('/webhook/stripe', data=stripe_payload, headers={"Stripe-Signature": "abc"})
            assert response.status_code == status.HTTP_200_OK
