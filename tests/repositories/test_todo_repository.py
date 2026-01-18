import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from exceptions import NotFoundError
from models import Todo, TodoUpdate
from src.repositories import todo_repository


async def test_find_all(session: AsyncSession, todo_factory):
    expected = await todo_factory(session)

    todos = await todo_repository.find_all(session)
    assert len(todos) == 1
    assert todos[0].title == "test todo"
    assert todos[0] == Todo.model_validate(expected)


async def test_find_by_id(session: AsyncSession, todo_factory):
    expected = await todo_factory(session)
    assert expected.id is not None

    found = await todo_repository.find_by_id(session, expected.id)
    assert found.id == expected.id
    assert found.title == "test todo"
    with pytest.raises(NotFoundError, match="Todo not found: id=999"):
        await todo_repository.find_by_id(session, 999)


async def test_find_by_query(session: AsyncSession, todo_factory):
    await todo_factory(session, title="foo", description="bar", completed=False)
    await todo_factory(session, title="baz", description="qux", completed=False)
    results = await todo_repository.find_by_query(session, "foo")
    assert len(results) == 1
    assert results[0].title == "foo"
    results = await todo_repository.find_by_query(session, "qux")
    assert len(results) == 1
    assert results[0].description == "qux"
    results = await todo_repository.find_by_query(session, "notfound")
    assert results == []


async def test_save(session: AsyncSession):
    todo = Todo(title="New Todo", description="desc", completed=False)
    saved = await todo_repository.save(session, todo)

    assert saved.id is not None
    assert saved.title == "New Todo"
    assert saved.description == "desc"
    assert saved.completed is False


async def test_update(session: AsyncSession, todo_factory):
    expected = await todo_factory(session, title="before", completed=False)
    assert expected.id is not None

    update = TodoUpdate(title="after", completed=True)
    updated = await todo_repository.update(session, expected.id, update)
    assert updated.title == "after"
    assert updated.completed is True


async def test_delete(session: AsyncSession, todo_factory):
    expected = await todo_factory(session, title="to delete", completed=False)
    assert expected.id is not None

    await todo_repository.delete(session, expected.id)
    assert await todo_repository.find_all(session) == []
    with pytest.raises(NotFoundError, match=f"Todo not found: id={expected.id}"):
        await todo_repository.find_by_id(session, expected.id)


async def test_count(session: AsyncSession, todo_factory):
    assert await todo_repository.count(session) == 0

    await todo_factory(session, title="one", description="desc", completed=False)
    await todo_factory(session, title="two", description="desc", completed=False)
    assert await todo_repository.count(session) == 2
