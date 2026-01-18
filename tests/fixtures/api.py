import pytest
from httpx import ASGITransport, AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from core.providers.db import get_db_session
from main import app


@pytest.fixture
async def client(session: AsyncSession):
    app.dependency_overrides[get_db_session] = lambda: session

    # Async TestClient equivalent
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
