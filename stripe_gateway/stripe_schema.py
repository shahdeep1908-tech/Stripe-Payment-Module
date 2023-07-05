from _decimal import Decimal
from enum import Enum

from pydantic import BaseModel


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
