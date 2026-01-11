import pytest
from pydantic import ValidationError

from models import Todo


def test_min_title_length():
    with pytest.raises(ValidationError):
        Todo(title="a", description="desc")


def test_max_description_length():
    long_desc = "x" * 501
    with pytest.raises(ValidationError):
        Todo(title="foo", description=long_desc)
