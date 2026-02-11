from functools import lru_cache
from typing import Annotated

import redis.asyncio as redis
from fastapi import Depends
from redis.asyncio.client import Redis

from core.settings.redis_settings import redis_settings


# singleton Redis client
@lru_cache
def get_redis_client() -> Redis:
    return redis.from_url(redis_settings.redis_url)  # pyright: ignore[reportUnknownMemberType]


RedisClient = Annotated[Redis, Depends(get_redis_client)]
