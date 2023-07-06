from fastapi import APIRouter
from stripe_gateway import stripe_router
from stripe_payment import payment_router

router = APIRouter()


@router.get('/')
def server_checkup():
    return "The server is running."


router.include_router(stripe_router.router)
router.include_router(payment_router.router)
