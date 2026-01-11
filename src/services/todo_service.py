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
    from sqlmodel import Session

    from core.types import FieldErrors

logger = get_logger()


def find_all_todos(session: Session) -> list[Todo]:
    return find_all(session)


def get_todo_form_dict(session: Session, todo_id: int) -> dict[str, str]:
    todo = find_by_id(session, todo_id)
    return {
        "title": todo.title,
        "description": todo.description,
        "completed": "on" if todo.completed else "",
    }


def search_todos(session: Session, query: str) -> list[Todo]:
    return find_by_query(session, query)


def add_todo(session: Session, todo: Todo) -> Todo:
    return save(session, todo)


def create_todo_from_form(
    session: Session, form_dict: dict[str, str]
) -> tuple[Todo, None] | tuple[None, FieldErrors]:
    try:
        form = TodoForm(**form_dict)
        data = form.to_model()
        todo = add_todo(session, data)
    except ValidationError as exc:
        logger.exception("Error parsing form data (create)")
        errors = group_errors_by_field(exc.errors())
        return None, errors
    else:
        return todo, None


def update_todo(session: Session, todo_id: int, data: Todo) -> Todo:
    todo_update = TodoUpdate(
        title=data.title,
        description=data.description or None,
        completed=data.completed,
    )
    return update(session, todo_id, todo_update)


def edit_todo_from_form(
    session: Session, todo_id: int, form_dict: dict[str, str]
) -> tuple[Todo, None] | tuple[None, FieldErrors]:
    try:
        form = TodoForm(**form_dict)
        data = form.to_model()
        todo = update_todo(session, todo_id, data)
    except ValidationError as exc:
        logger.exception("Error parsing form data (edit)")
        errors = group_errors_by_field(exc.errors())
        return None, errors
    else:
        return todo, None


async def set_todo_completed(
    session: Session, redis: Redis, todo_id: int, *, completed: bool
) -> Todo:
    todo_update = TodoUpdate(
        completed=completed,
    )  # type: ignore[call-arg]
    todo = update(session, todo_id, todo_update)

    event = _build_todo_completed_event(session)
    await publish_todo_completed_event(redis, event)

    return todo


async def remove_todo(session: Session, redis: Redis, todo_id: int) -> None:
    delete(session, todo_id)

    event = _build_todo_completed_event(session)
    await publish_todo_completed_event(redis, event)


def count_todos(session: Session) -> int:
    return count(session)


def count_completed_todos(session: Session) -> int:
    todos = find_all(session)
    return sum(1 for todo in todos if todo.completed)


def _build_todo_completed_event(session: Session) -> TodoCompletedEvent:
    done = count_completed_todos(session)
    total = count_todos(session)
    return TodoCompletedEvent(done=done, total=total)


async def event_generator(session: Session, redis: Redis) -> AsyncGenerator[str]:
    # push current count initially
    event = _build_todo_completed_event(session)
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
