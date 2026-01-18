import asyncio
from typing import TYPE_CHECKING

from pydantic_core import ValidationError

from core.logger import get_logger
from models import Todo, TodoCompletedEvent, TodoForm, TodoUpdate
from repositories.todo_repository import (
    count,
    delete,
    find_all,
    find_by_id,
    find_by_query,
    save,
    update,
)
from services.todo_pubsub import (
    publish_todo_completed_event,
    subscribe_todo_completed_event,
)
from utils.form_errors import group_errors_by_field

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from redis.asyncio.client import Redis
    from sqlmodel.ext.asyncio.session import AsyncSession

    from core.types import FieldErrors

logger = get_logger(__name__)


async def find_all_todos(session: AsyncSession) -> list[Todo]:
    return await find_all(session)


async def get_todo_form_dict(session: AsyncSession, todo_id: int) -> dict[str, str]:
    todo = await find_by_id(session, todo_id)
    return {
        "title": todo.title,
        "description": todo.description,
        "completed": "on" if todo.completed else "",
    }


async def search_todos(session: AsyncSession, query: str) -> list[Todo]:
    return await find_by_query(session, query)


async def add_todo(session: AsyncSession, todo: Todo) -> Todo:
    return await save(session, todo)


async def create_todo_from_form(
    session: AsyncSession, form_dict: dict[str, str]
) -> tuple[Todo, None] | tuple[None, FieldErrors]:
    try:
        form = TodoForm(**form_dict)
        data = form.to_model()
        todo = await add_todo(session, data)
    except ValidationError as exc:
        logger.exception("Error parsing form data (create)")
        errors = group_errors_by_field(exc.errors())
        return None, errors
    else:
        return todo, None


async def update_todo(session: AsyncSession, todo_id: int, data: Todo) -> Todo:
    todo_update = TodoUpdate(
        title=data.title,
        description=data.description or None,
        completed=data.completed,
    )
    return await update(session, todo_id, todo_update)


async def edit_todo_from_form(
    session: AsyncSession, todo_id: int, form_dict: dict[str, str]
) -> tuple[Todo, None] | tuple[None, FieldErrors]:
    try:
        form = TodoForm(**form_dict)
        data = form.to_model()
        todo = await update_todo(session, todo_id, data)
    except ValidationError as exc:
        logger.exception("Error parsing form data (edit)")
        errors = group_errors_by_field(exc.errors())
        return None, errors
    else:
        return todo, None


async def set_todo_completed(
    session: AsyncSession, redis: Redis, todo_id: int, *, completed: bool
) -> Todo:
    todo_update = TodoUpdate(
        completed=completed,
    )  # type: ignore[call-arg]
    todo = await update(session, todo_id, todo_update)

    event = await _build_todo_completed_event(session)
    await publish_todo_completed_event(redis, event)

    return todo


async def remove_todo(session: AsyncSession, redis: Redis, todo_id: int) -> None:
    await delete(session, todo_id)
    event = await _build_todo_completed_event(session)
    await publish_todo_completed_event(redis, event)


async def count_todos(session: AsyncSession) -> int:
    return await count(session)


async def count_completed_todos(session: AsyncSession) -> int:
    todos = await find_all(session)
    return sum(1 for todo in todos if todo.completed)


async def _build_todo_completed_event(session: AsyncSession) -> TodoCompletedEvent:
    done = await count_completed_todos(session)
    total = await count_todos(session)
    return TodoCompletedEvent(done=done, total=total)


async def event_generator(session: AsyncSession, redis: Redis) -> AsyncGenerator[str]:
    # push current count initially
    event = await _build_todo_completed_event(session)
    logger.info("Pushing initial todo completed event: %s", event)
    yield f"event: update\ndata: {event}\n\n"

    try:
        while True:
            # wait for new event from pubsub
            event = await subscribe_todo_completed_event(redis)
            logger.info("Pushing todo completed event: %s", event)
            yield f"event: update\ndata: {event}\n\n"
    except asyncio.CancelledError:
        logger.info("Event generator cancelled, exiting")
        raise
    finally:
        logger.info("Event generator cleanup complete")
