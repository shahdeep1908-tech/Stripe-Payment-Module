import json
from fastapi import status


class TestCreatePlan:
    def test_create_plan_success_201(self, client, stripe_create_plan_data, stripe_create_product):
        global product_id
        product_id = stripe_create_product
        stripe_create_plan_data['product_id'] = product_id

        response = client.post('/stripe/attach-plan', data=json.dumps(stripe_create_plan_data))
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['message'] == "Plan created successfully."

    def test_same_plan_with_different_interval_success_201(self, client, stripe_create_plan_data):
        stripe_create_plan_data['product_id'] = product_id
        stripe_create_plan_data['interval'] = "year"

        response = client.post('/stripe/attach-plan', data=json.dumps(stripe_create_plan_data))
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['message'] == "Plan created successfully."

    def test_same_plan_with_different_price_success_201(self, client, stripe_create_plan_data):
        stripe_create_plan_data['product_id'] = product_id
        stripe_create_plan_data['amount'] = 200

        response = client.post('/stripe/attach-plan', data=json.dumps(stripe_create_plan_data))
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['message'] == "Plan created successfully."

    def test_same_plan_with_different_currency_success_201(self, client, stripe_create_plan_data):
        stripe_create_plan_data['product_id'] = product_id
        stripe_create_plan_data['currency'] = "inr"

        response = client.post('/stripe/attach-plan', data=json.dumps(stripe_create_plan_data))
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['message'] == "Plan created successfully."

    def test_wrong_product_id_error_404(self, client, stripe_create_plan_data):
        response = client.post('/api/plan', data=json.dumps(stripe_create_plan_data))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_invalid_amount_error_422(self, client, stripe_create_plan_data):
        stripe_create_plan_data['product_id'] = product_id
        stripe_create_plan_data['amount'] = "abc"

        response = client.post('/stripe/attach-plan', data=json.dumps(stripe_create_plan_data))
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_invalid_interval_error_422(self, client, stripe_create_plan_data):
        stripe_create_plan_data['product_id'] = product_id
        stripe_create_plan_data['interval'] = "abc"

        response = client.post('/stripe/attach-plan', data=json.dumps(stripe_create_plan_data))
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_invalid_currency_error_422(self, client, stripe_create_plan_data):
        stripe_create_plan_data['product_id'] = product_id
        stripe_create_plan_data['currency'] = "abc"

        response = client.post('/stripe/attach-plan', data=json.dumps(stripe_create_plan_data))
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
