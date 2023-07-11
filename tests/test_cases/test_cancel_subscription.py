import json

from fastapi import status
from unittest.mock import patch


class TestUserCancelSubscriptionRoute:
    def test_invalid_subscription_id_404(self, client):
        subscription_id = "abc"
        data = {"reason": "Reactivating the subscription"}

        response = client.post(f'/stripe/cancel/{subscription_id}/subscription', data=json.dumps(data))
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_subscription_cancel_success_200(self, client):
        with patch("stripe_gateway.stripe_service.ProductPlanModel.cancel_subscription") as check_user_subscription:
            check_user_subscription.return_value = {"message": "Subscription recurring payment stop successfully",
                                                    'data': None}

            data = {"reason": "Reactivating the subscription"}

            subscription_id = "abc"
            response = client.post(f'/stripe/cancel/{subscription_id}/subscription', data=json.dumps(data))
            assert response.status_code == status.HTTP_200_OK
            assert response.json()['message'] == "Subscription recurring payment stop successfully"
