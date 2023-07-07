import stripe.error
from fastapi import APIRouter, Request, Response, Header, HTTPException, status

from common.app_logger import logger
from .webhook_authentication import verify_stripe_webhook_signature
from .webhook_schema import WebhookEndpointRequestSchema, ListCreteWebhookSchema
from .webhook_service import _stripe_webhook

from config import app_setting

router = APIRouter(tags=['Webhook'])


@router.post("/webhook/create-webhook", response_model=ListCreteWebhookSchema)
def create_webhook(request: WebhookEndpointRequestSchema, response: Response):
    return _stripe_webhook.create_webhook(request, response)


@router.post("/webhook/stripe")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    data = await request.body()
    try:
        event = verify_stripe_webhook_signature(payload=data, stripe_signature=stripe_signature)
        return await(_stripe_webhook.stripe_event_handler(event))
    except (ValueError, stripe.error.SignatureVerificationError) as err:
        logger.error(f"STRIPE VERIFICATION ERROR RAISED ::: {err}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)) from err
    except Exception as err:
        logger.error(f"EXCEPTION OCCURRED ::: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)) from err
