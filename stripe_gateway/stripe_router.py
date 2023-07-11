from fastapi import APIRouter, Response
from .stripe_service import _product_plan_model

from .stripe_schema import ProductRequestSchema, PlanRequestSchema, ListPlanSchema, CancelSubscriptionSchemaRequest, \
    CancelSubscriptionSchemaResponse

router = APIRouter(tags=['Stripe'])


@router.post('/stripe/create-product')
def stripe_create_product(request: ProductRequestSchema, response: Response):
    return _product_plan_model.create_product(request, response)


@router.post('/stripe/attach-plan')
def create_plan(request: PlanRequestSchema, response: Response):
    return _product_plan_model.create_plan(request, response)


@router.get('/stripe/plans', response_model=ListPlanSchema)
def list_plans(response: Response, limit: int | None = None):
    return _product_plan_model.list_plans(response, limit)


@router.post("/stripe/cancel/{sub_id}/subscription", response_model=CancelSubscriptionSchemaResponse)
async def cancel_subscription(sub_id: str, request: CancelSubscriptionSchemaRequest, response: Response):
    return await(_product_plan_model.cancel_subscription(sub_id, request, response))
