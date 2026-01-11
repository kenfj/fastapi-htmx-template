from typing import Annotated

from fastapi import APIRouter, Form, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from htmy import Component  # noqa: TC002 for FastAPI runtime type resolution

from core.logger import get_logger
from core.providers.context import (
    Context,  # noqa: TC001 for FastAPI runtime type resolution
)
from core.providers.db import (
    DbSession,  # noqa: TC001 for FastAPI runtime type resolution
)
from services.todo_service import (
    create_todo_from_form,
    edit_todo_from_form,
    event_generator,
    get_todo_form_dict,
    remove_todo,
    set_todo_completed,
)
from ui.components import todo_checkbox
from ui.pages import add_todo_html, edit_todo_html
from utils import html_endpoint, htmx_only, render_html
from utils.form_data import from_form_data

logger = get_logger()

router = APIRouter(prefix="/todos")


@router.get("/add", response_class=HTMLResponse, response_model=None)
@html_endpoint
async def show_add_todo_form() -> Component:
    return add_todo_html()


@router.post("/add")
async def create_todo(request: Request, ctx: Context) -> Response:
    form_data = await request.form()
    form_dict = from_form_data(form_data)
    todo, errors = create_todo_from_form(ctx.db, form_dict)

    if todo:
        hdr = {"X-Created-Todo-ID": str(todo.id)}
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER, headers=hdr)

    return HTMLResponse(
        content=await render_html(add_todo_html(form_dict, errors)),
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )


@router.get("/{todo_id}/edit", response_class=HTMLResponse, response_model=None)
@html_endpoint
async def show_edit_todo_form(todo_id: int, session: DbSession) -> Component:
    form_dict = get_todo_form_dict(session, todo_id)

    return edit_todo_html(todo_id, form_dict, {})


@router.post("/{todo_id}/edit")
async def edit_todo(request: Request, ctx: Context, todo_id: int) -> Response:
    form_data = await request.form()
    form_dict = from_form_data(form_data)
    todo, errors = edit_todo_from_form(ctx.db, todo_id, form_dict)

    if todo:
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

    return HTMLResponse(
        content=await render_html(edit_todo_html(todo_id, form_dict, errors)),
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )


@router.post("/{todo_id}/toggle_completed", response_class=HTMLResponse)
@htmx_only
async def toggle_completed_todo(
    _request: Request,  # required by htmx_only decorator
    ctx: Context,
    todo_id: int,
    *,
    # Note: If the checkbox is unchecked, 'completed' is not sent in the form data.
    # In that case, the default value (False) is used.
    completed: Annotated[bool, Form()] = False,
) -> HTMLResponse:
    todo = await set_todo_completed(ctx.db, ctx.redis, todo_id, completed=completed)
    checkbox = todo_checkbox(todo_id, completed=todo.completed)
    return HTMLResponse(content=await render_html(checkbox))


@router.get("/completed_count/stream")
async def completed_count_stream(ctx: Context) -> StreamingResponse:
    return StreamingResponse(
        event_generator(ctx.db, ctx.redis),
        media_type="text/event-stream",
    )


@router.delete("/{todo_id}")
@htmx_only
async def delete_todo(_request: Request, ctx: Context, todo_id: int) -> Response:
    logger.info("Deleting todo with ID: %d", todo_id)
    await remove_todo(ctx.db, ctx.redis, todo_id)
    return Response(content="", status_code=status.HTTP_200_OK)
