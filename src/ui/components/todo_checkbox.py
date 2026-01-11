from typing import TYPE_CHECKING

from htmy.html import input_

if TYPE_CHECKING:
    from htmy import ComponentType


def todo_checkbox(todo_id: int, *, completed: bool) -> ComponentType:
    return input_(
        type="checkbox",
        name="completed",
        **({"checked": True} if completed else {}),
        hx_post=f"/todos/{todo_id}/toggle_completed",
        hx_trigger="change",
        hx_target="this",
        hx_swap="outerHTML",
        style="margin-right:0.5em;",
    )
