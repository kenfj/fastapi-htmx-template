import textwrap
from io import BytesIO

from fastapi import UploadFile
from fastapi.datastructures import FormData
from pydantic_core import ErrorDetails

from core.types import FieldErrors
from utils import render_html
from utils.form_data import from_form_data
from utils.form_errors import group_errors_by_field, make_error_ul


def test_group_errors_by_field():
    errors: list[ErrorDetails] = [
        ErrorDetails(
            loc=("body", "title"),
            msg="required",
            type="value_error.missing",
            input=None,
        ),
        ErrorDetails(
            loc=("body", "desc"), msg="too short", type="value_error.short", input=""
        ),
        ErrorDetails(
            loc=("body", "title"), msg="invalid", type="value_error", input=""
        ),
    ]
    grouped = group_errors_by_field(errors)

    assert set(grouped.keys()) == {"title", "desc"}
    assert len(grouped["title"]) == 2
    assert grouped["desc"][0]["msg"] == "too short"


def test_group_errors_empty():
    errors: list[ErrorDetails] = []
    grouped = group_errors_by_field(errors)

    assert grouped == {}


def test_to_form_dict_basic():
    form = FormData(
        [
            ("a", "x"),
            ("b", "123"),
            ("c", ""),
            ("d", UploadFile(filename="dummy.txt", file=BytesIO(b""))),
        ]
    )
    result = from_form_data(form)

    assert result == {
        "a": "x",
        "b": "123",
        "c": "",
        "d": "",
    }


async def test_make_error_ul_html():
    errors: FieldErrors = {
        "title": [
            ErrorDetails(
                loc=("body", "title"),
                msg="required",
                type="value_error.missing",
                input=None,
            ),
            ErrorDetails(
                loc=("body", "title"), msg="invalid", type="value_error", input=""
            ),
        ]
    }
    error_ul = make_error_ul(errors)
    ul_elem = error_ul("title")

    assert ul_elem is not None

    html = await render_html(ul_elem)

    assert html == textwrap.dedent("""\
        <ul >
        <li style="color:red;">required</li>
        <li style="color:red;">invalid</li>
        </ul>""")

    ul_none = error_ul("description")
    assert ul_none is None


def test_make_error_ul_none():
    error_ul = make_error_ul(None)
    assert error_ul("any_field") is None


def test_make_error_ul_empty_dict():
    error_ul = make_error_ul({})
    assert error_ul("any_field") is None


def test_make_error_ul_field_not_present():
    errors: FieldErrors = {
        "field1": [
            ErrorDetails(
                loc=("body", "field1"),
                msg="dummy",
                type="value_error",
                input="",
            )
        ]
    }
    error_ul = make_error_ul(errors)
    assert error_ul("field2") is None


def test_make_error_ul_empty_list():
    errors: FieldErrors = {"field1": []}
    error_ul = make_error_ul(errors)
    assert error_ul("field1") is None
