import json
from fastapi import status


class TestCreateProduct:
    def test_create_product_success_201(self, client, stripe_create_product_data):
        response = client.post('/stripe/create-product', data=json.dumps(stripe_create_product_data))
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['message'] == "Product created successfully"

    def test_invalid_product_name_500(self, client, stripe_create_product_data):
        stripe_create_product_data['name'] = "a" * 300

        response = client.post('/stripe/create-product', data=json.dumps(stripe_create_product_data))
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

