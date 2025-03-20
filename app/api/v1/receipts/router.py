from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.v1.auth.models import AuthenticationModel, RegisterCredentialsModel, UserResponseModel
from app.api.v1.exceptions.already_exists import AlreadyExistsError
from app.api.v1.exceptions.invalid_credentials import InvalidCredentialsError
from app.api.v1.receipts.models import ReceiptModel, CreateReceiptModel
from app.api.v1.security.authenticator import Authenticator
from app.database.models import User
from app.dependencies import database_session

receipts_router: APIRouter = APIRouter(prefix="/receipts", tags=["Receipts"])


@receipts_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ReceiptModel,
)
async def create_receipt(
        receipt: CreateReceiptModel,
        user: Annotated[User, Authenticator.get_user()],
        session: Annotated[AsyncSession, Depends(database_session)],
) -> ReceiptModel:
    pass
