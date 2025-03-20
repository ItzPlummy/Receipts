from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

from app.database.models import PaymentType, Receipt


class ProductModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(max_length=50)
    price: Decimal = Field(gt=0)
    quantity: int = Field(default=1, gt=0)
    total: Decimal = Field(gt=0)


class PaymentModel(BaseModel):
    type: PaymentType
    amount: Decimal = Field(gt=0)


class ReceiptModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    products: List[ProductModel]
    payment: PaymentModel
    total: Decimal
    rest: Decimal

    created_at: datetime
    updated_at: datetime | None = None

    @property
    def total(self) -> Decimal:
        return Decimal(sum(product.total for product in self.products))

    @property
    def rest(self) -> Decimal:
        return self.payment.amount - self.total

    @classmethod
    def from_database_model(cls, receipt: Receipt) -> 'ReceiptModel':
        return cls(
            id=receipt.id,
            products=receipt.products,
            payment=PaymentModel(type=receipt.payment_type, amount=receipt.payment_amount),
            total=receipt.total,
            rest=receipt.rest,
            created_at=receipt.created_at,
            updated_at=receipt.updated_at,
        )


class CreateProductModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(max_length=50)
    price: Decimal = Field(gt=0)
    quantity: int = Field(default=1, gt=0)

    @property
    def total(self) -> Decimal:
        return self.price * self.quantity


class CreateReceiptModel(BaseModel):
    products: List[CreateProductModel]
    payment: PaymentModel

    @property
    def total(self) -> Decimal:
        return Decimal(sum(product.total for product in self.products))

    @property
    def rest(self) -> Decimal:
        return self.payment.amount - self.total
