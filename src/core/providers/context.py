from typing import TYPE_CHECKING, Annotated

from fastapi.params import Depends

from core.providers.db import (
    DbSession,  # noqa: TC001 for FastAPI runtime type resolution
)
from core.providers.redis import (
    RedisClient,  # noqa: TC001 for FastAPI runtime type resolution
)

if TYPE_CHECKING:
    from redis.asyncio.client import Redis
    from sqlmodel.ext.asyncio.session import AsyncSession


class AppContext:
    def __init__(self, db_session: AsyncSession, redis_client: Redis) -> None:
        self.db = db_session
        self.redis = redis_client


def get_context(db_session: DbSession, redis_client: RedisClient) -> AppContext:
    return AppContext(db_session, redis_client)


Context = Annotated[AppContext, Depends(get_context)]
