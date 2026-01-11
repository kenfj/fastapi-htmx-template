from typing import TYPE_CHECKING

from redis.asyncio.client import Redis

from core.logger import get_logger
from models import TodoCompletedEvent

if TYPE_CHECKING:
    from redis.asyncio.client import PubSub, Redis

logger = get_logger()

# official example: https://redis.readthedocs.io/en/stable/examples/asyncio_examples.html
# pyright: reportUnknownMemberType=false

_CHANNEL: str = "todo_completed"


async def publish_todo_completed_event(redis: Redis, event: TodoCompletedEvent) -> None:
    logger.info("Publishing todo completed event: %s", event)
    message = event.model_dump_json()
    num = await redis.publish(channel=_CHANNEL, message=message)
    logger.info("Published todo completed event to %d subscribers", num)


async def _reader(pubsub: PubSub) -> TodoCompletedEvent:
    while True:
        message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=None)  # pyright: ignore[reportUnknownVariableType]
        if message is not None and message["type"] == "message":
            return TodoCompletedEvent.model_validate_json(message["data"])  # pyright: ignore[reportUnknownArgumentType]


async def subscribe_todo_completed_event(redis: Redis) -> TodoCompletedEvent:
    async with redis.pubsub() as pubsub:
        await pubsub.subscribe(_CHANNEL)
        return await _reader(pubsub)
