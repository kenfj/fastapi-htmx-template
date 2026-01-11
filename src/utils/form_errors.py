from typing import TYPE_CHECKING

from htmy.html import li, ul

if TYPE_CHECKING:
    from collections.abc import Callable

    from htmy import ComponentType
    from pydantic_core import ErrorDetails

    from core.types import FieldErrors


def group_errors_by_field(errors: list[ErrorDetails]) -> FieldErrors:
    grouped: FieldErrors = {}

    for error in errors:
        field = error["loc"][-1]
        grouped.setdefault(field, []).append(error)

    return grouped


def make_error_ul(errors: FieldErrors | None) -> Callable[[str], ComponentType | None]:
    def error_ul(field: str) -> ComponentType | None:
        if errors and errors.get(field):
            return ul(
                *[li(error["msg"], style="color:red;") for error in errors[field]]
            )
        return None

    return error_ul
