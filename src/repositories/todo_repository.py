from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import func, or_
from sqlmodel import Session, select

from exceptions import NotFoundError
from models import TodoEntity, TodoUpdate

if TYPE_CHECKING:
    from models import Todo


def find_all(session: Session) -> list[Todo]:
    entities = session.exec(select(TodoEntity)).all()
    return [entity.to_model() for entity in entities]


def find_by_id(session: Session, todo_id: int) -> Todo:
    entity = session.get(TodoEntity, todo_id)
    if not entity:
        msg = f"Todo not found: id={todo_id}"
        raise NotFoundError(msg)
    return entity.to_model()


def find_by_query(session: Session, query: str) -> list[Todo]:
    statement = select(TodoEntity).where(
        or_(
            func.lower(TodoEntity.title).like(f"%{query.lower()}%"),
            func.lower(TodoEntity.description).like(f"%{query.lower()}%"),
        )
    )
    entities = session.exec(statement).all()
    return [entity.to_model() for entity in entities]


def _find_entity_by_id(session: Session, todo_id: int) -> TodoEntity:
    entity = session.get(TodoEntity, todo_id)
    if not entity:
        msg = f"Todo not found: id={todo_id}"
        raise NotFoundError(msg)
    return entity


def save(session: Session, todo: Todo) -> Todo:
    """Upsert a TodoEntity"""
    entity = TodoEntity.from_model(todo)
    session.add(entity)

    session.commit()
    session.refresh(entity)
    return entity.to_model()


def update(session: Session, todo_id: int, update_data: TodoUpdate) -> Todo:
    entity = _find_entity_by_id(session, todo_id)
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(entity, key, value)
    entity.updated_at = datetime.now(UTC)

    session.commit()
    session.refresh(entity)
    return entity.to_model()


def delete(session: Session, todo_id: int) -> None:
    entity = _find_entity_by_id(session, todo_id)
    session.delete(entity)
    session.commit()


def count(session: Session) -> int:
    statement = select(func.count()).select_from(TodoEntity)
    return session.exec(statement).one()
