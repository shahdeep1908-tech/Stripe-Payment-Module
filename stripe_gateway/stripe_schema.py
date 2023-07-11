from _decimal import Decimal
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class ResponseMessage(BaseModel):
    message: str


class ProductRequestSchema(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True
        extra = 'forbid'


class IntervalChoices(Enum):
    day: str = "day"
    week: str = "week"
    month: str = "month"
    year: str = "year"


class CurrencyChoices(Enum):
    USD: str = "usd"
    INR: str = "inr"


class PlanRequestSchema(BaseModel):
    product_id: str
    name: str
    amount: Decimal
    interval: IntervalChoices
    currency: CurrencyChoices

    class Config:
        orm_mode = True
        extra = 'forbid'


class PlanResponseSchema(BaseModel):
    id: str
    product: str
    nickname: Optional[str]
    active: bool
    interval: str

    class Config:
        orm_mode = True


class ListPlanSchema(ResponseMessage):
    data: Optional[List[PlanResponseSchema]]


class CancelSubscriptionSchemaRequest(BaseModel):
    reason: str

    class Config:
        orm_mode = True


class CancelSubscriptionSchemaResponse(ResponseMessage):
    data: Optional[str]

    class Config:
        orm_mode = True
