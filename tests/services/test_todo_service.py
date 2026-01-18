from sqlmodel.ext.asyncio.session import AsyncSession

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


async def test_get_todo_form_dict_returns_expected_dict(mocker, session: AsyncSession):
    todo = Todo(id=1, title="foo", description="bar", completed=True)
    mocker.patch("services.todo_service.find_by_id", return_value=todo)

    todo_id = 1
    form_dict = await get_todo_form_dict(session, todo_id)

    assert form_dict == {"title": "foo", "description": "bar", "completed": "on"}


async def test_get_todo_form_dict_returns_expected_dict2(mocker, session: AsyncSession):
    todo = Todo(id=1, title="foo", description="", completed=False)
    mocker.patch("services.todo_service.find_by_id", return_value=todo)

    todo_id = 1
    form_dict = await get_todo_form_dict(session, todo_id)

    assert form_dict == {"title": "foo", "description": "", "completed": ""}


async def test_add_todo(session: AsyncSession):
    form = Todo(title="Test Todo", description="desc", completed=False)
    todo = await add_todo(session, form)
    assert todo.id is not None
    assert todo.title == "Test Todo"
    assert todo.description == "desc"
    assert todo.completed is False
    assert await count_todos(session) == 1


async def test_create_todo_from_form_success(mocker):
    todo_obj = mocker.Mock()
    mocker.patch("services.todo_service.add_todo", return_value=todo_obj)
    mocker.patch("services.todo_service.TodoForm", return_value=mocker.Mock())

    session = mocker.Mock()
    form_dict = {"title": "foo", "description": "bar", "completed": "on"}
    todo, errors = await create_todo_from_form(session, form_dict)

    assert todo is todo_obj
    assert errors is None


async def test_create_todo_from_form_validation_error(mocker):
    session = mocker.Mock()
    form_dict = {
        "title": "a",
        "description": "bar",
        "completed": "on",
    }

    todo, errors = await create_todo_from_form(session, form_dict)
    assert todo is None
    assert errors is not None
    assert errors.get("title") is not None
    assert errors["title"][0]["type"] == "string_too_short"
    assert errors["title"][0]["loc"] == ("title",)
    assert errors["title"][0]["msg"] == "String should have at least 3 characters"
    assert errors["title"][0]["input"] == "a"


async def test_update_todo(session: AsyncSession):
    form = Todo(title="Test", description="desc", completed=False)
    todo = await add_todo(session, form)
    assert todo.id is not None

    update_form = Todo(title="Updated", description="new desc", completed=True)
    updated = await update_todo(session, todo.id, update_form)
    assert updated.title == "Updated"
    assert updated.description == "new desc"
    assert updated.completed is True


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


async def test_count_completed_todos(session: AsyncSession):
    await add_todo(session, Todo(title="AAA", completed=True))
    await add_todo(session, Todo(title="BBB", completed=False))
    await add_todo(session, Todo(title="CCC", completed=True))
    assert await count_todos(session) == 3
    assert await count_completed_todos(session) == 2


async def test_event_generator_pushes_on_pubsub(mocker, session: AsyncSession):
    redis = mocker.Mock()
    await add_todo(session, Todo(title="Test", completed=False))

    mocker.patch(
        "services.todo_service.subscribe_todo_completed_event",
        mocker.AsyncMock(return_value=TodoCompletedEvent(done=5, total=100)),
    )

    gen = event_generator(session, redis)

    # check initial yield
    first = await gen.__anext__()
    assert first == "event: update\ndata: 0 / 1 Completed\n\n"

    # check subsequent yield after pubsub event
    second = await gen.__anext__()
    assert second == "event: update\ndata: 5 / 100 Completed\n\n"

    # close generator
    await gen.aclose()
