from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from core.logger import get_logger
from exceptions import NotFoundError
from models import ErrorResponse

logger = get_logger(__name__)

ERROR_LOG_FORMAT = "%s occurred: %s"


def http_exception_handler(_request: Request, exc: HTTPException) -> JSONResponse:
    response = ErrorResponse.from_exception(exc)
    logger.error(ERROR_LOG_FORMAT, response.error, response.model_dump())

    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump(exclude={"trace"}),
    )


def not_found_error_handler(_request: Request, exc: NotFoundError) -> JSONResponse:
    response = ErrorResponse.from_exception(exc)
    logger.error(ERROR_LOG_FORMAT, response.error, response.model_dump())

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=response.model_dump(exclude={"trace"}),
    )


def sqlalchemy_error_handler(_request: Request, exc: SQLAlchemyError) -> JSONResponse:
    response = ErrorResponse.from_exception(exc)
    logger.error(ERROR_LOG_FORMAT, response.error, response.model_dump())

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response.model_dump(exclude={"trace"}),
    )


def generic_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    response = ErrorResponse.from_exception(exc)
    logger.error(ERROR_LOG_FORMAT, response.error, response.model_dump())

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response.model_dump(exclude={"trace"}),
    )


# pyright: reportArgumentType=false
def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(NotFoundError, not_found_error_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
