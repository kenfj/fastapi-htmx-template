"""
Logger setup:

 - Production: JSON format
 - Development: single-line text format
 - Includes filename and line number in log output
"""

import logging
import logging.config

from core.settings import settings

JSON_FORMATTER = "pythonjsonlogger.jsonlogger.JsonFormatter"


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def setup_logging() -> None:
    formatter = JSON_FORMATTER if settings.log_format == "json" else "default"

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s %(name)s [%(levelname)s] %(filename)s:%(lineno)d %(message)s",  # noqa: E501
            },
            JSON_FORMATTER: {
                "format": "%(asctime)s %(name)s %(levelname)s %(filename)s %(lineno)d %(message)s",  # noqa: E501
                "class": JSON_FORMATTER,
            },
        },
        "handlers": {
            "console": {
                "formatter": formatter,
                "class": "logging.StreamHandler",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": settings.log_level,
        },
        "loggers": {
            "uvicorn": {
                "handlers": ["console"],
                "level": settings.log_level,
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["console"],
                "level": settings.log_level,
                "propagate": False,
            },
            "uvicorn.error": {
                "handlers": ["console"],
                "level": settings.log_level,
                "propagate": False,
            },
            "sqlalchemy.engine": {
                "handlers": ["console"],
                "level": settings.log_level,
                "propagate": False,
            },
            "app": {
                "handlers": ["console"],
                "level": settings.log_level,
                "propagate": False,
            },
        },
    }
    logging.config.dictConfig(logging_config)
