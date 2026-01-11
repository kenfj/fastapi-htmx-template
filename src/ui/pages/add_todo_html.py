from typing import TYPE_CHECKING

from htmy.html import a, button, form, h1, section

from ui.components import app_layout, todo_form_fields

if TYPE_CHECKING:
    from htmy import Component

    from core.types import FieldErrors


def add_todo_html(
    form_dict: dict[str, str] | None = None,
    errors: FieldErrors | None = None,
) -> Component:
    content = section(
        h1("Add Todo"),
        form(
            todo_form_fields(form_dict, errors),
            button("Add", type="submit"),
            method="post",
            action="/todos/add",
        ),
        a("Back", href="/", role="button"),
    )

    return app_layout([content], page_title="Add Todo")
