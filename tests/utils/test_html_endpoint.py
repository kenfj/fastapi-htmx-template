import asyncio

from fastapi.responses import HTMLResponse
from htmy import Component, SafeStr
from htmy.html import body, head, html, title

from utils.html_endpoint import html_endpoint


async def dummy_page() -> Component:
    await asyncio.sleep(0)
    return (SafeStr("<!DOCTYPE html>"), html(head(title("Test")), body("Hello")))


async def test_html_endpoint_returns_html_response():
    decorated = html_endpoint(dummy_page)
    response = await decorated()

    assert isinstance(response, HTMLResponse)
    assert "Hello" in bytes(response.body).decode()
    assert response.status_code == 200
