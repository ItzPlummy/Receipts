from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.v1.auth.models import AuthenticationModel, RegisterCredentialsModel
from app.api.v1.exceptions.already_exists import AlreadyExistsError
from app.api.v1.exceptions.invalid_credentials import InvalidCredentialsError
from app.api.v1.security.authenticator import Authenticator
from app.database.models import User
from app.dependencies import database_session

auth_router: APIRouter = APIRouter(prefix="/auth", tags=["Authorization"])


@auth_router.post(
    "/",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=AuthenticationModel,
)
async def login(
        credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Annotated[AsyncSession, Depends(database_session)],
        authenticator: Annotated[Authenticator, Depends(Authenticator.dependency)],
) -> AuthenticationModel:
    user: User | None = await session.scalar(
        select(User)
        .filter_by(email=credentials.username)
    )

    if user is None or not await authenticator.verify_password(credentials.password, user.password_hash):
        raise InvalidCredentialsError("Provided credentials are invalid")

    access_token: str = await authenticator.create_access_token(user.id)

    return AuthenticationModel(access_token=access_token)


@auth_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=AuthenticationModel,
)
async def register(
        credentials: RegisterCredentialsModel,
        session: Annotated[AsyncSession, Depends(database_session)],
        authenticator: Annotated[Authenticator, Depends(Authenticator.dependency)],
) -> AuthenticationModel:
    user: User = User(
        username=credentials.username,
        email=credentials.email,
        password_hash=await authenticator.hash_password(credentials.password),
    )
    session.add(user)

    try:
        await session.commit()
    except IntegrityError:
        raise AlreadyExistsError("User with provided credentials already exists.")

    access_token: str = await authenticator.create_access_token(user.id)

    return AuthenticationModel(access_token=access_token)
