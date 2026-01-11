from pydantic import BaseModel

from models import Todo


class TodoForm(BaseModel):
    """
    DTO for validating and holding form input values when creating or editing a item.

    Used for form validation, error redisplay, and conversion to the application model.
    """

    title: str
    description: str = ""
    completed: str | None = None

    def to_model(self) -> Todo:
        return Todo(
            title=self.title,
            description=self.description,
            completed=(self.completed == "on"),
        )
