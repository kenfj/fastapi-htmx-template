from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import func, or_
from sqlmodel import select

from exceptions import NotFoundError
from models import TodoEntity, TodoUpdate

if TYPE_CHECKING:
    from sqlmodel.ext.asyncio.session import AsyncSession

    from models import Todo


async def find_all(session: AsyncSession) -> list[Todo]:
    results = await session.exec(select(TodoEntity))
    entities = results.all()
    return [entity.to_model() for entity in entities]


async def find_by_id(session: AsyncSession, todo_id: int) -> Todo:
    entity = await session.get(TodoEntity, todo_id)
    if not entity:
        msg = f"Todo not found: id={todo_id}"
        raise NotFoundError(msg)
    return entity.to_model()


async def find_by_query(session: AsyncSession, query: str) -> list[Todo]:
    statement = select(TodoEntity).where(
        or_(
            func.lower(TodoEntity.title).like(f"%{query.lower()}%"),
            func.lower(TodoEntity.description).like(f"%{query.lower()}%"),
        )
    )
    results = await session.exec(statement)
    entities = results.all()
    return [entity.to_model() for entity in entities]


async def _find_entity_by_id(session: AsyncSession, todo_id: int) -> TodoEntity:
    entity = await session.get(TodoEntity, todo_id)
    if not entity:
        msg = f"Todo not found: id={todo_id}"
        raise NotFoundError(msg)
    return entity


async def save(session: AsyncSession, todo: Todo) -> Todo:
    """Upsert a TodoEntity"""
    entity = TodoEntity.from_model(todo)
    session.add(entity)

    await session.commit()
    await session.refresh(entity)
    return entity.to_model()


async def update(session: AsyncSession, todo_id: int, update_data: TodoUpdate) -> Todo:
    entity = await _find_entity_by_id(session, todo_id)
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(entity, key, value)
    entity.updated_at = datetime.now(UTC)

    await session.commit()
    await session.refresh(entity)
    return entity.to_model()


async def delete(session: AsyncSession, todo_id: int) -> None:
    entity = await _find_entity_by_id(session, todo_id)
    await session.delete(entity)
    await session.commit()


async def count(session: AsyncSession) -> int:
    statement = select(func.count()).select_from(TodoEntity)
    results = await session.exec(statement)
    return results.one()
