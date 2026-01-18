from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from core.exception_handlers import register_exception_handlers
from core.lifespan import lifespan
from core.logger import get_logger, setup_logging
from core.settings import settings
from routers import root_router, todo_router

setup_logging()

logger = get_logger(__name__)

logger.info("Starting application: %s", settings.app_env)

app = FastAPI(lifespan=lifespan)

static_dir = Path(__file__).parent.parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.include_router(root_router.router)
app.include_router(todo_router.router)

register_exception_handlers(app)
