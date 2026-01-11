from pydantic_core import ErrorDetails

FieldErrors = dict[int | str, list[ErrorDetails]]
"""
FieldErrors: Type for storing pydantic validation errors per field.
Keys are str (normal field names) or int (array/nested index).
Example: errors["title"], errors[0], errors["items"], errors["user"]
"""
