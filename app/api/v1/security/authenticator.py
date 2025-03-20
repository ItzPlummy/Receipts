import asyncio
from datetime import datetime, timedelta
from typing import Dict, Annotated
from uuid import UUID

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import encode, decode, InvalidTokenError
from pytz import utc
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.exceptions.invalid_access_token import InvalidAccessTokenError
from app.api.v1.exceptions.invalid_credentials import InvalidCredentialsError
from app.database.models import User
from app.dependencies import config_dependency, database_session
from config import Config


class Authenticator:
    ACCESS_TOKEN_EXPIRE = timedelta(minutes=15)
    OAUTH_SCHEME: OAuth2PasswordBearer = OAuth2PasswordBearer("/api/v1/auth/")

    def __init__(
            self,
            *,
            jwt_key: str,
            jwt_algorithm: str
    ) -> None:
        self.__jwt_key = jwt_key
        self.__jwt_algorithm = jwt_algorithm
        self.__ph = PasswordHasher()

    async def hash_password(
            self,
            password: str
    ) -> str:
        return await asyncio.to_thread(self.__ph.hash, password)

    async def verify_password(
            self,
            password: str,
            password_hash: str
    ) -> bool:
        try:
            await asyncio.to_thread(self.__ph.verify, password_hash, password)
            return True
        except VerifyMismatchError:
            return False

    async def create_access_token(
            self,
            user_id: UUID
    ) -> str:
        return await asyncio.to_thread(
            encode,
            {
                "id": str(user_id),
                "exp": datetime.now(utc) + self.ACCESS_TOKEN_EXPIRE,
                "mode": "access",
            },
            self.__jwt_key,
            self.__jwt_algorithm
        )

    async def decode_access_token(
            self,
            access_token: str
    ) -> Dict[str, str]:
        try:
            token: Dict[str, str] = await asyncio.to_thread(
                decode,
                access_token,
                self.__jwt_key,
                [self.__jwt_algorithm],
            )
        except InvalidTokenError:
            raise InvalidAccessTokenError("Provided token is invalid or expired")

        if "id" not in token or "mode" not in token or token.get("mode") != "access":
            raise InvalidAccessTokenError("Provided token is invalid")

        return token

    async def verify_access_token(
            self,
            access_token: str,
            session: AsyncSession
    ) -> User:
        data: Dict[str, str] = await self.decode_access_token(access_token)

        try:
            user_id: UUID = UUID(data["id"])
        except ValueError:
            raise InvalidCredentialsError("Provided credentials are invalid")

        user: User | None = await session.scalar(
            select(User)
            .filter_by(id=user_id)
        )

        if user is None:
            raise InvalidCredentialsError("Provided credentials are invalid")

        return user

    @staticmethod
    def dependency(config: Annotated[Config, Depends(config_dependency)]) -> 'Authenticator':
        return Authenticator(
            jwt_key=config.jwt_key.get_secret_value(),
            jwt_algorithm=config.jwt_algorithm
        )

    @classmethod
    def get_user(cls) -> Depends:
        async def __get_user(
                access_token: Annotated[str, Depends(cls.OAUTH_SCHEME)],
                session: Annotated[AsyncSession, Depends(database_session)],
                authenticator: Annotated[Authenticator, Depends(Authenticator.dependency)]
        ) -> User:
            return await authenticator.verify_access_token(access_token, session)

        return Depends(__get_user)
