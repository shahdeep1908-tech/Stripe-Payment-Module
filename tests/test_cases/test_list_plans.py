from unittest.mock import patch

from fastapi import status


class TestListPlan:
    def test_get_plan_success_200(self, client, create_plan):
        response = client.get('/stripe/plans')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['message'] == "All plans fetched successfully"

    def test_without_any_plan_200(self, client):
        with patch("stripe_gateway.stripe_service.StripePaymentHandler.list_plans") as list_plans:
            list_plans.return_value = None

            response = client.get('/stripe/plans')
            assert response.status_code == status.HTTP_200_OK
            assert response.json()['message'] == "No plans available."
