import pytest
from inline_snapshot import snapshot

from ui.components import todo_form_fields
from utils import render_html


@pytest.mark.asyncio
async def test_todo_form_fields_default():
    html = await render_html(todo_form_fields())

    assert html == snapshot("""\
<fieldset >
<label htmlFor="title">
Title
</label>
<input type="text" name="title" id="title" value="" required="true" placeholder="Title"/>
<label htmlFor="description">
Description
</label>
<textarea name="description" id="description" placeholder="Description"></textarea>
<label htmlFor="completed">
Completed
</label>
<input type="checkbox" name="completed" id="completed"/>
</fieldset>\
""")


@pytest.mark.asyncio
async def test_todo_form_fields_completed():
    form_dict = {
        "title": "foo",
        "completed": "on",
    }
    html = await render_html(todo_form_fields(form_dict))

    assert html == snapshot("""\
<fieldset >
<label htmlFor="title">
Title
</label>
<input type="text" name="title" id="title" value="foo" required="true" placeholder="Title"/>
<label htmlFor="description">
Description
</label>
<textarea name="description" id="description" placeholder="Description"></textarea>
<label htmlFor="completed">
Completed
</label>
<input type="checkbox" name="completed" id="completed" checked="checked"/>
</fieldset>\
""")
