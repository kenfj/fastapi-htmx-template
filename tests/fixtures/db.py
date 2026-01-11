import pytest
from sqlmodel import Session, create_engine

from core.providers.db import get_db_session, init_db
from main import app


@pytest.fixture
def test_db_engine():
    """
    In-memory DB for repository/service layer tests.

    Tables are created fresh for each test function and discarded afterwards.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        echo=False,
        connect_args={"check_same_thread": False},
    )
    init_db(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def test_db_session(test_db_engine):
    """
    Session for in-memory DB for repository/service layer tests.

    Used to provide a clean database session for each test function.
    """
    with Session(test_db_engine) as session:
        yield session


@pytest.fixture(autouse=True)
def override_db_session(tmp_path):
    """
    Provide a database session for API (routes) layer tests using a temporary file DB.

    Why file DB?
    SQLite's in-memory DB cannot be shared across multiple connections.
    FastAPI's dependency injection creates a new DB session/connection for each request,
    so in-memory DB would result in isolated, empty databases per request.
    Using a file-based DB allows all sessions to share the same data,
    making it suitable for API tests that need persistent test data.
    """
    db_path = tmp_path / "test_api.db"
    engine = create_engine(
        f"sqlite:///{db_path}",
        echo=False,
        connect_args={"check_same_thread": False},
    )
    init_db(engine)

    def get_test_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_db_session] = get_test_session
    yield
    app.dependency_overrides.clear()
    engine.dispose()
