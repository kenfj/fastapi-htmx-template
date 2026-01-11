from contextlib import suppress

import sqlalchemy
from sqlmodel import Session

from core.providers.db import get_db_session, get_engine


def test_get_engine_returns_engine():
    engine = get_engine()

    assert engine is not None
    assert isinstance(engine, sqlalchemy.engine.Engine)


def test_get_db_session_yields_session():
    engine = get_engine()
    gen = get_db_session(engine)
    session = next(gen)

    assert isinstance(session, Session)
    # generator should close session after use
    with suppress(StopIteration):
        next(gen)
