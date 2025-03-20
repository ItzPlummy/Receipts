from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field

from app.database.models import PaymentType


class ProductModel(BaseModel):
    name: str = Field(max_length=50)
    price: Decimal = Field(gt=0)
    quantity: int = Field(default=1, gt=0)

    @property
    def total(self) -> Decimal:
        return self.price * self.quantity


class PaymentModel(BaseModel):
    type: PaymentType
    amount: Decimal = Field(gt=0)


class ReceiptModel(BaseModel):
    id: UUID
    products: List[ProductModel]
    payment: PaymentModel
    total: Decimal
    rest: Decimal

    created_at: datetime
    updated_at: datetime | None = None


class CreateReceiptModel(BaseModel):
    products: List[ProductModel]
    payment: PaymentModel
