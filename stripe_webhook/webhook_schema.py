from typing import Optional

from pydantic import BaseModel


class ResponseMessage(BaseModel):
    message: str


class WebhookEndpointRequestSchema(BaseModel):
    webhook_endpoint: Optional[str] = "/webhook/stripe"
    description: str = "This is my first Stripe webhook"
    events: Optional[list] = ['*']

    class Config:
        orm_mode = True


class CreateWebhookResponseSchema(BaseModel):
    id: str
    description: Optional[str]
    enabled_events: list
    status: str
    url: str

    class Config:
        orm_mode = True


class ListCreteWebhookSchema(ResponseMessage):
    data: Optional[CreateWebhookResponseSchema]