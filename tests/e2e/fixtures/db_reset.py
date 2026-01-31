import pytest
from sqlmodel import text

from core.providers.db import async_engine


@pytest.fixture(autouse=True)
async def reset_db():
    async with async_engine.begin() as conn:
        await conn.execute(text("DELETE FROM todo"))
