from typing import TYPE_CHECKING

from htmy.html import a, div, h1, li, p, section, span, ul

from services.todo_service import count_completed_todos, count_todos, find_all_todos
from ui.components import app_layout, todo_checkbox

if TYPE_CHECKING:
    from htmy import Component
    from sqlmodel.ext.asyncio.session import AsyncSession


async def index_html(session: AsyncSession) -> Component:
    todos = await find_all_todos(session)
    total = await count_todos(session)
    done = await count_completed_todos(session)

    if todos:
        todo_list = ul(
            *[
                li(
                    todo_checkbox(todo.id, completed=todo.completed),
                    span(todo.title, style="font-weight:bold;"),
                    span(todo.description or "", style="color:gray;"),
                    a(
                        "✏️",
                        href=f"/todos/{todo.id}/edit",
                        title="Edit",
                        aria_label="Edit",
                        tabindex="0",
                        style="text-decoration:none; font-size:1.2em;",
                    ),
                    span(
                        "🗑️",
                        hx_delete=f"/todos/{todo.id}",
                        hx_target="closest li",
                        hx_swap="delete swap:1s",
                        title="Delete",
                        aria_label="Delete",
                        tabindex="0",
                        style="cursor:pointer; font-size:1.2em;",
                    ),
                    class_="todo-row",
                )
                for todo in todos
                if todo.id is not None
            ],
        )
    else:
        todo_list = p("No todos.")

    page_content = [
        section(
            h1("Todo List"),
            div(
                p(
                    f"{done} / {total} Completed",
                    id="completed-count",
                    hx_ext="sse",
                    sse_connect="/todos/completed_count/stream",
                    sse_swap="update",
                ),
                a(
                    "Add Todo",
                    href="/todos/add",
                    role="button",
                    style="margin-left:auto;",
                ),
                style="display:flex;",
            ),
        ),
        section(
            todo_list,
        ),
    ]

    return app_layout(page_content, page_title="Todo List")
