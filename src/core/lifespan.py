from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from core.app_env_config import APP_ENV
from core.providers.db import get_engine, init_db
from enums import AppEnv

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from fastapi import FastAPI


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
    # startup code
    if APP_ENV == AppEnv.development:
        engine = get_engine()
        init_db(engine)
        engine.dispose()
    yield
    # shutdown code
