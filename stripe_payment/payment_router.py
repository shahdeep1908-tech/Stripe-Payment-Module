from fastapi import APIRouter, Request

from config import templates
from stripe_payment.payment_service import checkout_payment_session, customer_service_portal

router = APIRouter(tags=['payment'])


def initialize_session():
    from main import app
    return app


@router.get("/subscribe")
def index(request: Request):
    app = initialize_session()
    return templates.TemplateResponse("index.html",
                                      context={'request': request,
                                               'isCustomer': app.state.stripe_customer_id is not None})


@router.get("/success")
async def success(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})


@router.get("/cancel")
async def cancel(request: Request):
    return templates.TemplateResponse("cancel.html", {"request": request})


@router.post("/create-checkout-session")
async def create_session_checkout(request: Request):
    app = initialize_session()
    return await checkout_payment_session(request, app)


@router.post("/customer-portal")
async def customer_portal():
    app = initialize_session()
    return await customer_service_portal(app)