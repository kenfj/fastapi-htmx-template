import pytest

from exceptions import NotFoundError
from models import Todo, TodoUpdate
from src.repositories import todo_repository


def test_save_and_find_all(test_db_session, todo_factory):
    expected = todo_factory(test_db_session)

    todos = todo_repository.find_all(test_db_session)
    assert len(todos) == 1
    assert todos[0].title == "test todo"
    assert todos[0] == Todo.model_validate(expected)


def test_find_by_id(test_db_session, todo_factory):
    expected = todo_factory(test_db_session)
    assert expected.id is not None

    found = todo_repository.find_by_id(test_db_session, expected.id)
    assert found.id == expected.id
    assert found.title == "test todo"
    with pytest.raises(NotFoundError, match="Todo not found: id=999"):
        todo_repository.find_by_id(test_db_session, 999)


def test_find_by_query(test_db_session, todo_factory):
    todo_factory(test_db_session, title="foo", description="bar", completed=False)
    todo_factory(test_db_session, title="baz", description="qux", completed=False)

    results = todo_repository.find_by_query(test_db_session, "foo")
    assert len(results) == 1
    assert results[0].title == "foo"
    results = todo_repository.find_by_query(test_db_session, "qux")
    assert len(results) == 1
    assert results[0].description == "qux"
    results = todo_repository.find_by_query(test_db_session, "notfound")
    assert results == []


def test_update(test_db_session, todo_factory):
    expected = todo_factory(test_db_session, title="before", completed=False)
    assert expected.id is not None

    update = TodoUpdate(title="after", completed=True)
    updated = todo_repository.update(test_db_session, expected.id, update)
    assert updated.title == "after"
    assert updated.completed is True


def test_delete(test_db_session, todo_factory):
    expected = todo_factory(test_db_session, title="to delete", completed=False)
    assert expected.id is not None

    todo_repository.delete(test_db_session, expected.id)
    assert todo_repository.find_all(test_db_session) == []
    with pytest.raises(NotFoundError, match=f"Todo not found: id={expected.id}"):
        todo_repository.find_by_id(test_db_session, expected.id)


def test_count(test_db_session, todo_factory):
    assert todo_repository.count(test_db_session) == 0

    todo_factory(test_db_session, title="one", description="desc", completed=False)
    todo_factory(test_db_session, title="two", description="desc", completed=False)

    assert todo_repository.count(test_db_session) == 2
