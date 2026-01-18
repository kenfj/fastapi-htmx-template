from inline_snapshot import snapshot

from ui.components import todo_checkbox
from utils import render_html


async def test_todo_checkbox_unchecked():
    html = await render_html(todo_checkbox(1, completed=False))
    assert html == snapshot(
        '<input type="checkbox" name="completed" hx-post="/todos/1/toggle_completed" hx-trigger="change" hx-target="this" hx-swap="outerHTML" style="margin-right:0.5em;"/>'
    )


async def test_todo_checkbox_checked():
    html = await render_html(todo_checkbox(2, completed=True))
    assert html == snapshot(
        '<input type="checkbox" name="completed" checked="true" hx-post="/todos/2/toggle_completed" hx-trigger="change" hx-target="this" hx-swap="outerHTML" style="margin-right:0.5em;"/>'
    )
