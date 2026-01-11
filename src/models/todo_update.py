from typing import Annotated

from annotated_types import Len
from pydantic import BaseModel

from core.constants import MAX_DESCRIPTION_LENGTH, MIN_TITLE_LENGTH


class TodoUpdate(BaseModel):
    title: Annotated[str | None, Len(min_length=MIN_TITLE_LENGTH)] = None
    description: Annotated[str | None, Len(max_length=MAX_DESCRIPTION_LENGTH)] = None
    completed: bool | None = None
