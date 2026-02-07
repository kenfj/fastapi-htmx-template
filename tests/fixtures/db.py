import tempfile

import pytest
from anyio import Path as AsyncPath
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.fixture(scope="session")  # Session scope for engine, function scope for session
async def engine():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:  # NOSONAR
        temp_path = tmp.name

    test_db_url = f"sqlite+aiosqlite:///{temp_path}"

    # Use NullPool for testing to disable pooling
    async_engine = create_async_engine(
        test_db_url,
        connect_args={"check_same_thread": False},  # For SQLite
        poolclass=NullPool,  # Disable connection pooling for isolation
    )
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)  # Create tables

    yield async_engine

    await async_engine.dispose()  # Clean up engine
    if await AsyncPath(temp_path).exists():
        await AsyncPath(temp_path).unlink()


@pytest.fixture  # function scope by default
async def session(engine):
    async with engine.connect() as conn, conn.begin() as transaction:
        async_session_maker = async_sessionmaker(
            bind=conn, class_=AsyncSession, expire_on_commit=False
        )

        async with async_session_maker() as async_session:
            yield async_session

        # rollback/cleanup after each test to prevent auto-commit
        await transaction.rollback()
