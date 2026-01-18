import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from models import Todo
from repositories import todo_repository


@pytest.fixture
def todo_factory():
    async def _create(
        session: AsyncSession,
        title="test todo",
        description="desc",
        *,
        completed=False,
    ) -> Todo:
        todo = Todo(title=title, description=description, completed=completed)
        return await todo_repository.save(session, todo)

    return _create
