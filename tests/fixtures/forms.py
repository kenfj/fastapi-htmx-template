import pytest

from models import TodoForm


@pytest.fixture
def todo_form_checked():
    return TodoForm(title="task", description="desc", completed="on")


@pytest.fixture
def todo_form_unchecked():
    return TodoForm(title="task", description="desc", completed=None)
