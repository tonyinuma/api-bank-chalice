from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field


class Currency(str, Enum):
    PEN = "PEN"
    USD = "USD"


class AccountStatus(str, Enum):
    ACTIVE = "active"
    BLOCKED = "blocked"


class AccountCreate(BaseModel):
    customer_name: str = Field(
        min_length=2,
        max_length=100,
    )
    currency: Currency


class AccountResponse(BaseModel):
    id: int
    customer_name: str
    currency: Currency
    status: AccountStatus
    balance: Decimal


class DepositRequest(BaseModel):
    amount: Decimal = Field(
        gt=0,
        decimal_places=2,
    )