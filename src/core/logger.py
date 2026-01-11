"""
Logger setup:

 - Production: JSON format
 - Development: single-line text format
 - Includes filename and line number in log output
"""

from typing import TYPE_CHECKING

import structlog

from core.app_env_config import APP_ENV
from core.settings import settings

if TYPE_CHECKING:
    from structlog.stdlib import BoundLogger
    from structlog.typing import EventDict, Processor


def simple_renderer(_logger: BoundLogger, _method_name: str, events: EventDict) -> str:
    return (
        f"{events['timestamp']} [{events['level'].upper()}] "
        f"{events['filename']}:{events['lineno']} "
        f"{events['event']}"
    )


def init_logger() -> None:
    processors: list[Processor] = [
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.LINENO,
            }
        ),
    ]
    if APP_ENV == "production":
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(simple_renderer)

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(settings.log_level.value),
        cache_logger_on_first_use=True,
    )


def get_logger() -> BoundLogger:
    return structlog.get_logger()
