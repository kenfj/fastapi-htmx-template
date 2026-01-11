import pytest
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.testclient import TestClient

from utils.htmx_only import _get_request_or_raise, htmx_only

app = FastAPI()


@app.get("/htmx")
@htmx_only
async def htmx_endpoint(_request: Request):
    return {"ok": True}


def test_htmx_only_allows_htmx_request():
    client = TestClient(app)
    response = client.get("/htmx", headers={"HX-Request": "true"})
    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_htmx_only_rejects_non_htmx_request():
    client = TestClient(app)
    response = client.get("/htmx")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "htmx request required"


def test_extract_request_from_args():
    req = Request(scope={"type": "http"})
    # Should return the Request instance from args
    assert _get_request_or_raise((req,), {}) is req


def test_extract_request_from_kwargs():
    req = Request(scope={"type": "http"})
    # Should return the Request instance from kwargs
    assert _get_request_or_raise((), {"request": req}) is req


def test_extract_request_from_kwargs_with_underscore():
    req = Request(scope={"type": "http"})
    # Should return the Request instance from kwargs with '_request' key
    assert _get_request_or_raise((), {"_request": req}) is req


class DummyRequest:
    pass


dummy = DummyRequest()


def test_extract_request_raises_if_missing():
    # Should raise HTTPException if no Request instance is found
    with pytest.raises(HTTPException) as excinfo:
        _get_request_or_raise((dummy,), {})
    assert excinfo.value.status_code == status.HTTP_400_BAD_REQUEST
    assert "Request object missing" in excinfo.value.detail


def test_extract_request_raises_if_kwargs_not_request_type():
    with pytest.raises(HTTPException) as excinfo:
        _get_request_or_raise((), {"request": dummy})
    assert excinfo.value.status_code == status.HTTP_400_BAD_REQUEST
    assert "Request object missing" in excinfo.value.detail
