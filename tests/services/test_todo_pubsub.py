import pytest

from models import TodoCompletedEvent
from services.todo_pubsub import (
    publish_todo_completed_event,
    subscribe_todo_completed_event,
)


@pytest.mark.asyncio
async def test_pubsub_publish_and_subscribe_mocked(pubsub_mocks):
    redis, pubsub = pubsub_mocks

    event = TodoCompletedEvent(done=3, total=7)
    pubsub.get_message.return_value = {
        "type": "message",
        "data": event.model_dump_json(),
    }

    await publish_todo_completed_event(redis, event)
    redis.publish.assert_awaited_once_with(
        channel="todo_completed", message=event.model_dump_json()
    )

    received = await subscribe_todo_completed_event(redis)
    assert isinstance(received, TodoCompletedEvent)
    assert received.done == 3
    assert received.total == 7
