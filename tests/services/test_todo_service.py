import pytest

from models import Todo, TodoCompletedEvent
from services.todo_service import (
    add_todo,
    count_completed_todos,
    count_todos,
    create_todo_from_form,
    event_generator,
    get_todo_form_dict,
    set_todo_completed,
    update_todo,
)


def test_get_todo_form_dict_returns_expected_dict(mocker, test_db_session):
    todo = Todo(id=1, title="foo", description="bar", completed=True)
    mocker.patch("services.todo_service.find_by_id", return_value=todo)

    todo_id = 1
    form_dict = get_todo_form_dict(test_db_session, todo_id)

    assert form_dict == {"title": "foo", "description": "bar", "completed": "on"}


def test_get_todo_form_dict_returns_expected_dict2(mocker, test_db_session):
    todo = Todo(id=1, title="foo", description="", completed=False)
    mocker.patch("services.todo_service.find_by_id", return_value=todo)

    todo_id = 1
    form_dict = get_todo_form_dict(test_db_session, todo_id)

    assert form_dict == {"title": "foo", "description": "", "completed": ""}


def test_add_todo(test_db_session):
    form = Todo(title="Test Todo", description="desc", completed=False)
    todo = add_todo(test_db_session, form)
    assert todo.id is not None
    assert todo.title == "Test Todo"
    assert todo.description == "desc"
    assert todo.completed is False
    assert count_todos(test_db_session) == 1


def test_create_todo_from_form_success(mocker):
    todo_obj = mocker.Mock()
    mocker.patch("services.todo_service.add_todo", return_value=todo_obj)
    mocker.patch("services.todo_service.TodoForm", return_value=mocker.Mock())

    session = mocker.Mock()
    form_dict = {"title": "foo", "description": "bar", "completed": "on"}
    todo, errors = create_todo_from_form(session, form_dict)

    assert todo is todo_obj
    assert errors is None


def test_create_todo_from_form_validation_error(mocker):
    session = mocker.Mock()
    form_dict = {
        "title": "a",
        "description": "bar",
        "completed": "on",
    }

    todo, errors = create_todo_from_form(session, form_dict)
    assert todo is None
    assert errors is not None
    assert errors.get("title") is not None
    assert errors["title"][0]["type"] == "string_too_short"
    assert errors["title"][0]["loc"] == ("title",)
    assert errors["title"][0]["msg"] == "String should have at least 3 characters"
    assert errors["title"][0]["input"] == "a"


def test_update_todo(test_db_session):
    form = Todo(title="Test", description="desc", completed=False)
    todo = add_todo(test_db_session, form)
    assert todo.id is not None

    update_form = Todo(title="Updated", description="new desc", completed=True)
    updated = update_todo(test_db_session, todo.id, update_form)
    assert updated.title == "Updated"
    assert updated.description == "new desc"
    assert updated.completed is True


@pytest.mark.asyncio
async def test_set_todo_completed(mocker):
    session = mocker.Mock()
    redis = mocker.Mock()

    # start with completed is False
    todo = Todo(id=1, title="Test", completed=False)
    updated_todo = Todo(id=1, title="Test", completed=True)
    assert todo.id is not None

    mocker.patch("services.todo_service.find_by_id", return_value=todo)
    mocker.patch("services.todo_service.update", return_value=updated_todo)
    mocker.patch("services.todo_service.find_all", return_value=[updated_todo])
    mocker.patch("services.todo_service.count", return_value=1)

    pubsub_mock = mocker.AsyncMock()
    mocker.patch("services.todo_service.publish_todo_completed_event", pubsub_mock)

    # execute: change completed to True
    result = await set_todo_completed(session, redis, todo.id, completed=True)

    assert isinstance(result, Todo)
    assert result.completed is True
    pubsub_mock.assert_awaited_once()


def test_count_completed_todos(test_db_session):
    add_todo(test_db_session, Todo(title="AAA", completed=True))
    add_todo(test_db_session, Todo(title="BBB", completed=False))
    add_todo(test_db_session, Todo(title="CCC", completed=True))
    assert count_todos(test_db_session) == 3
    assert count_completed_todos(test_db_session) == 2


@pytest.mark.asyncio
async def test_event_generator_pushes_on_pubsub(mocker, test_db_session):
    redis = mocker.Mock()
    add_todo(test_db_session, Todo(title="Test", completed=False))

    mocker.patch(
        "services.todo_service.subscribe_todo_completed_event",
        mocker.AsyncMock(return_value=TodoCompletedEvent(done=5, total=100)),
    )

    gen = event_generator(test_db_session, redis)

    # check initial yield
    first = await gen.__anext__()
    assert first == "event: update\ndata: 0 / 1 Completed\n\n"

    # check subsequent yield after pubsub event
    second = await gen.__anext__()
    assert second == "event: update\ndata: 5 / 100 Completed\n\n"

    # close generator
    await gen.aclose()
