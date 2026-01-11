import pytest


@pytest.fixture(autouse=True)
def mock_pubsub_repository(mocker):
    mocker.patch(
        "services.todo_service.publish_todo_completed_event",
        mocker.AsyncMock(),
    )
    mocker.patch(
        "services.todo_service.subscribe_todo_completed_event",
        mocker.AsyncMock(),
    )
