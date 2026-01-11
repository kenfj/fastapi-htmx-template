from typing import TYPE_CHECKING

from htmy.html import fieldset, input_, label, textarea

from core.logger import get_logger
from utils.form_errors import make_error_ul

if TYPE_CHECKING:
    from htmy import ComponentType

    from core.types import FieldErrors

logger = get_logger()


def todo_form_fields(
    form_dict: dict[str, str] | None = None,
    errors: FieldErrors | None = None,
) -> ComponentType:
    form_dict = form_dict or {}
    errors = errors or {}
    error_ul = make_error_ul(errors)

    logger.info("todo_form_fields: form_dict=%s and errors=%s", form_dict, errors)

    elements = [
        label("Title", htmlFor="title"),
        input_(
            type="text",
            name="title",
            id="title",
            value=form_dict.get("title", ""),
            required=True,
            placeholder="Title",
        ),
        error_ul("title"),
        label("Description", htmlFor="description"),
        textarea(
            *([form_dict["description"]] if form_dict.get("description") else []),
            name="description",
            id="description",
            placeholder="Description",
        ),
        error_ul("description"),
        label("Completed", htmlFor="completed"),
        input_(
            type="checkbox",
            name="completed",
            id="completed",
            **{"checked": "checked"} if form_dict.get("completed") == "on" else {},
        ),
        error_ul("completed"),
    ]

    # filter out None when error_ul returns None
    return fieldset(*[el for el in elements if el is not None])
