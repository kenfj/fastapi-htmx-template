from collections.abc import Generator  # noqa: TC003 for FastAPI runtime type resolution
from typing import Annotated

from fastapi import Depends
from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, create_engine

from core.settings import settings


def init_db(db_engine: Engine) -> None:
    """Create all database tables for development/testing purposes."""
    SQLModel.metadata.create_all(db_engine)


def get_engine() -> Engine:
    return create_engine(settings.db_url)


_DbEngine = Annotated[Engine, Depends(get_engine)]


def get_db_session(engine: _DbEngine) -> Generator[Session]:
    with Session(engine) as session:
        yield session


DbSession = Annotated[Session, Depends(get_db_session)]
