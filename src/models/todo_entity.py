from datetime import UTC, datetime

from sqlmodel import Field, SQLModel  # type: ignore[reportUnknownMemberType]

from core.constants import MAX_DESCRIPTION_LENGTH, MIN_TITLE_LENGTH
from models import Todo


class TodoEntity(SQLModel, table=True):
    # custom table name: https://github.com/fastapi/sqlmodel/issues/159
    __tablename__: str = "todo"  #  pyright: ignore[reportIncompatibleVariableOverride]

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(..., min_length=MIN_TITLE_LENGTH)
    description: str | None = Field(default=None, max_length=MAX_DESCRIPTION_LENGTH)
    completed: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = Field(default=None)

    def to_model(self) -> Todo:
        data = self.model_dump(exclude_none=True)
        data["description"] = self.description or ""  # None to empty string
        return Todo(**data)

    @classmethod
    def from_model(cls, todo: Todo) -> TodoEntity:
        data = todo.model_dump(exclude_none=True)
        data["description"] = todo.description or None  # empty string to None
        return TodoEntity(**data)
