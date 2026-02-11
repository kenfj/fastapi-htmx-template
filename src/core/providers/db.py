from collections.abc import (
    AsyncGenerator,  # noqa: TC003 for FastAPI runtime type resolution
)
from typing import Annotated

from fastapi import Depends
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from core.settings.db_settings import db_settings

IS_SQLITE = db_settings.db_url.startswith("sqlite")

connect_args = {"check_same_thread": False} if IS_SQLITE else {}
engine_kwargs = {"poolclass": NullPool} if IS_SQLITE else {}

async_engine = create_async_engine(
    db_settings.db_url,
    echo=db_settings.db_echo,
    connect_args=connect_args,
    **engine_kwargs,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session


DbSession = Annotated[AsyncSession, Depends(get_db_session)]
