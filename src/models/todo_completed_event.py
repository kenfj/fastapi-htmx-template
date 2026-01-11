from pydantic import BaseModel


class TodoCompletedEvent(BaseModel):
    done: int
    total: int

    def __str__(self) -> str:
        return f"{self.done} / {self.total} Completed"
