from typing import TYPE_CHECKING

from fastapi import UploadFile

if TYPE_CHECKING:
    from fastapi.datastructures import FormData


def from_form_data(form: FormData) -> dict[str, str]:
    """
    Convert FormData to a dict of str values for safe form re-display.

    - UploadFile and None are always converted to an empty string ("").
    - All other values are converted to str.
    """
    result: dict[str, str] = {}

    for k, v in form.items():
        if isinstance(v, str):
            result[k] = v.strip()
        elif isinstance(v, UploadFile):
            result[k] = ""
        else:
            result[k] = str(v)

    return result
