import pytest

from models import Todo
from repositories import todo_repository


@pytest.fixture
def todo_factory():
    def _create(
        session,
        title="test todo",
        description="desc",
        *,
        completed=False,
    ) -> Todo:
        todo = Todo(title=title, description=description, completed=completed)
        return todo_repository.save(session, todo)

    return _create
