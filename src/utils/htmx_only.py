import functools
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING

from fastapi import HTTPException, Request, status

if TYPE_CHECKING:
    from collections.abc import Mapping


FuncType = Callable[..., Awaitable[object]]
"""
Type alias for a standard FastAPI async endpoint function:
accepts any arguments and returns an awaitable object
"""


def htmx_only(func: FuncType) -> FuncType:
    # Copy func's metadata (name, docstring, etc.) to wrapper
    @functools.wraps(func)
    async def wrapper(*args: tuple[object], **kwargs: dict[str, object]) -> object:
        request = _get_request_or_raise(args, kwargs)

        if request.headers.get("HX-Request") != "true":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="htmx request required",
            )

        return await func(*args, **kwargs)

    return wrapper


def _get_request_or_raise(
    args: tuple[object, ...],
    kwargs: Mapping[str, object],
) -> Request:
    for arg in args:
        if isinstance(arg, Request):
            return arg

    request = kwargs.get("request") or kwargs.get("_request")

    if not isinstance(request, Request):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request object missing",
        )

    return request
