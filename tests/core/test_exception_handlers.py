from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

from core.exception_handlers import register_exception_handlers
from exceptions import NotFoundError

app = FastAPI()
register_exception_handlers(app)


@app.get("/raise_http")
def raise_http():
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="bad request")


@app.get("/raise_notfound")
def raise_notfound():
    msg = "The requested resource was not found."
    raise NotFoundError(msg)


@app.get("/raise_sqlalchemy")
def raise_sqlalchemy():
    msg = "This is a generic SQLAlchemy error"
    raise SQLAlchemyError(msg)


@app.get("/raise_generic")
def raise_generic():
    msg = "This is a generic exception"
    raise Exception(msg)  # NOSONAR # noqa: TRY002


def test_http_exception_handler():
    client = TestClient(app)
    resp = client.get("/raise_http")
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json() == {
        "error": "HTTPException",
        "detail": "bad request",
    }


def test_not_found_error_handler():
    client = TestClient(app)
    resp = client.get("/raise_notfound")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert resp.json() == {
        "error": "NotFoundError",
        "detail": "The requested resource was not found.",
    }


def test_sqlalchemy_error_handler():
    client = TestClient(app)
    resp = client.get("/raise_sqlalchemy")
    assert resp.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert resp.json() == {
        "error": "SQLAlchemyError",
        "detail": "This is a generic SQLAlchemy error",
    }


def test_generic_exception_handler():
    client = TestClient(app, raise_server_exceptions=False)
    resp = client.get("/raise_generic")
    assert resp.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert resp.json() == {
        "error": "Exception",
        "detail": "This is a generic exception",
    }
