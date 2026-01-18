from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from sqlmodel import SQLModel

from core.providers.db import async_engine
from core.settings import settings
from enums.app_env import AppEnv

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from fastapi import FastAPI


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
    # startup code
    if settings.app_env in (AppEnv.DEVELOPMENT, AppEnv.TEST):
        async with async_engine.begin() as conn:
            # Create all database tables for development/testing purposes.
            # run_sync calls sync function within async context
            await conn.run_sync(SQLModel.metadata.create_all)
    yield
    # shutdown code
