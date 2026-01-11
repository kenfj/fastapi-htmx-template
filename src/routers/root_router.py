from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from htmy import Component  # noqa: TC002 for FastAPI runtime type resolution

from core.providers.context import (
    Context,  # noqa: TC001 for FastAPI runtime type resolution
)
from ui.pages import index_html
from utils.html_endpoint import html_endpoint

router = APIRouter()


@router.get("/", response_class=HTMLResponse, response_model=None)
@html_endpoint
async def root(ctx: Context) -> Component:
    return index_html(ctx.db)
