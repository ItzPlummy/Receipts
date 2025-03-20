from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from app.database.database import Database
from config import Config


async def config_dependency(request: Request) -> Config:
    return request.app.state.config


async def database_dependency(request: Request) -> Database:
    return request.app.state.database


async def database_session(
        database: Annotated[Database, Depends(database_dependency)]
) -> AsyncGenerator[AsyncSession, None]:
    async with database.session_maker() as session:
        yield session
