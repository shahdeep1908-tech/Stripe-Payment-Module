from _decimal import Decimal

from fastapi import status
from fastapi.encoders import jsonable_encoder
from stripe import Product, Plan
from stripe.error import StripeError

from common.app_logger import logger
from common.exceptions import StripeException


class ProductPlanModel:
    @staticmethod
    def create_product(request, response):
        message, data = "", None
        try:
            product_response = _stripe_payment_handler.create_product(name=request.name,
                                                                      description=request.description)
            data = {
                'id': product_response.get('id'),
                'name': product_response.get('name'),
                'description': product_response.get('description'),
                'meta_data': product_response
            }
            message = "Product created successfully"
        except (StripeException, Exception) as err:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = str(err)
            logger.error(f"EXCEPTION OCCURRED WHILE CREATING PRODUCT ::: {err}")
        return {'message': message, 'data': data}

    @staticmethod
    def create_plan(request, response):
        message, data = "", None
        request_data = jsonable_encoder(request)
        try:
            plan_response = _stripe_payment_handler.create_plan(
                product_id=request_data.get("product_id"),
                name=request_data.get("name"),
                amount=request_data.get("amount"),
                interval=request_data.get("interval"),
                currency=request_data.get("currency")
            )

            data = {
                'id': plan_response.get('id'),
                'name': plan_response.get('nickname'),
                'interval': plan_response.get('interval'),
                'currency': plan_response.get('currency'),
                'product_id': plan_response.get('product_id'),
                'amount': plan_response.get('amount'),
                'meta_data': plan_response
            }
            message = "Plan created successfully."
        except (StripeException, Exception) as err:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = str(err)
            logger.error(f"EXCEPTION OCCURRED WHILE CREATING PLAN ::: {err}")
        return {'message': message, 'data': data}

    @staticmethod
    def list_plans(response, limit):
        message, data = "No plans available.", None
        try:
            if available_plans := _stripe_payment_handler.list_plans(limit=limit):
                data = available_plans.data
                message = "All plans fetched successfully"
        except (StripeException, Exception) as err:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = str(err)
            logger.error(f"ERROR OCCURRED WHILE LISTING PLANS ::: {err}")
        return {'message': message, 'data': data}


class StripePaymentHandler:
    @staticmethod
    def create_product(name: str, description: str):
        try:
            return Product.create(name=name, description=description)
        except StripeError as err:
            raise StripeException(f"Product not created ::: {err}") from err

    @staticmethod
    def create_plan(product_id: str, name: str, amount: Decimal, interval: str, currency: str):
        try:
            return Plan.create(product=product_id, nickname=name, amount=amount, interval=interval, currency=currency)
        except StripeError as err:
            raise StripeException(f"Plan not created ::: {err}") from err

    @staticmethod
    def list_plans(limit):
        try:
            return Plan.list(limit=limit)
        except StripeError as err:
            raise StripeException(f"Error in Listing Plan ::: {err}") from err


_product_plan_model = ProductPlanModel()
_stripe_payment_handler = StripePaymentHandler()
