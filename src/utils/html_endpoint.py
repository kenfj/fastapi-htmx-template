import functools
from collections.abc import Awaitable, Callable

from fastapi.responses import HTMLResponse
from htmy import Component

from .render import render_html

FuncComponent = Callable[..., Awaitable[Component]]
"""async function returning Component"""


def html_endpoint(func: FuncComponent) -> Callable[..., Awaitable[HTMLResponse]]:
    @functools.wraps(func)
    async def wrapper(*args: object, **kwargs: object) -> HTMLResponse:
        page = await func(*args, **kwargs)
        result = await render_html(page)
        return HTMLResponse(content=result)

    return wrapper
