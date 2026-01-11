import traceback

from fastapi import HTTPException
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    error: str
    detail: str
    trace: str | None = None

    @classmethod
    def from_exception(cls, exc: Exception) -> ErrorResponse:
        return cls(
            error=exc.__class__.__name__,
            detail=exc.detail if isinstance(exc, HTTPException) else str(exc),
            trace="".join(
                traceback.format_exception(type(exc), exc, exc.__traceback__)
            ),
        )
