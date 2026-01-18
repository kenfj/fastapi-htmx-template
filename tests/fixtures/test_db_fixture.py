from sqlmodel import text
from sqlmodel.ext.asyncio.session import AsyncSession


async def test_database_connection(session: AsyncSession):
    value = await session.scalar(text("SELECT 1"))
    assert value == 1


def test_hello_world():
    assert 1 + 1 == 2
