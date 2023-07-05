from fastapi import APIRouter
from stripe_gateway import stripe_router

router = APIRouter()


@router.get('/')
def server_checkup():
    return "The server is running."


router.include_router(stripe_router.router)
