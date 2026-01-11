from typing import TYPE_CHECKING

from htmy.html import a, button, form, h1, section

from ui.components import app_layout, todo_form_fields

if TYPE_CHECKING:
    from htmy import Component

    from core.types import FieldErrors


def edit_todo_html(
    todo_id: int,
    form_dict: dict[str, str],
    errors: FieldErrors | None,
) -> Component:
    content = section(
        h1("Edit Todo"),
        form(
            todo_form_fields(form_dict, errors),
            button("Update", type="submit"),
            method="post",
            action=f"/todos/{todo_id}/edit",
        ),
        a("Back", href="/", role="button"),
    )

    return app_layout([content], page_title="Edit Todo")
