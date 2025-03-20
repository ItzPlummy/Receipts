from typing import Annotated, Sequence

from fastapi import APIRouter, Depends
from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette import status

from app.api.v1.exceptions.invalid_payment_amount import InvalidPaymentAmountError
from app.api.v1.models.pagination import PaginationParams, PaginatedResult
from app.api.v1.receipts.models import ReceiptModel, CreateReceiptModel
from app.api.v1.security.authenticator import Authenticator
from app.database.models import User, Receipt, Product
from app.dependencies import database_session

receipts_router: APIRouter = APIRouter(prefix="/receipts", tags=["Receipts"])


@receipts_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ReceiptModel,
)
async def create_receipt(
        receipt_model: CreateReceiptModel,
        user: Annotated[User, Authenticator.get_user()],
        session: Annotated[AsyncSession, Depends(database_session)],
) -> ReceiptModel:
    if receipt_model.payment.amount < receipt_model.total:
        raise InvalidPaymentAmountError("Payment amount cannot be less than total amount")

    receipt: Receipt = Receipt(
        user_id=user.id,
        payment_type=receipt_model.payment.type,
        payment_amount=receipt_model.payment.amount,
        total=receipt_model.total,
        rest=receipt_model.rest
    )
    session.add(receipt)
    await session.commit()

    for product in receipt_model.products:
        session.add(
            Product(
                receipt_id=receipt.id,
                name=product.name,
                price=product.price,
                quantity=product.quantity,
                total=product.total,
            )
        )
    await session.commit()

    receipt: Receipt = await session.scalar(
        select(Receipt)
        .filter_by(id=receipt.id)
        .options(joinedload(Receipt.products))
    )

    return ReceiptModel.from_database_model(receipt)


@receipts_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedResult[ReceiptModel],
)
async def get_all_receipts(
        pagination: Annotated[PaginationParams, Depends()],
        user: Annotated[User, Authenticator.get_user()],
        session: Annotated[AsyncSession, Depends(database_session)],
) -> PaginatedResult[ReceiptModel]:
    query: Select = pagination.apply(select(Receipt)).filter_by(user_id=user.id)

    receipts: Sequence[Receipt] = (
        await session.execute(
            query.options(joinedload(Receipt.products))
        )
    ).unique().scalars().all()

    return pagination.create_response(
        results=[ReceiptModel.from_database_model(receipt) for receipt in receipts],
        model=ReceiptModel,
    )
