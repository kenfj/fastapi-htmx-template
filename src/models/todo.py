from datetime import datetime  # noqa: TC003 for Pydantic v2 runtime type resolution
from typing import Annotated

from annotated_types import Len
from pydantic import BaseModel, ConfigDict

from core.constants import MAX_DESCRIPTION_LENGTH, MIN_TITLE_LENGTH


class Todo(BaseModel):
    id: int | None = None
    title: Annotated[str, Len(min_length=MIN_TITLE_LENGTH)]
    # receive empty string for empty description as per html form spec
    description: Annotated[str, Len(max_length=MAX_DESCRIPTION_LENGTH)] = ""
    completed: bool = False
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True,  # allow population by ORM objects
    )
