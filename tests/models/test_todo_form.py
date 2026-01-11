import pytest

from models import Todo, TodoForm


def test_todo_form_to_model_empty_description():
    form = TodoForm(title="task", completed="on")
    model = form.to_model()
    assert model.description == ""


def test_todo_form_to_model_checked(todo_form_checked):
    model = todo_form_checked.to_model()

    assert isinstance(model, Todo)
    assert model.title == "task"
    assert model.description == "desc"
    assert model.completed is True


def test_todo_form_to_model_unchecked(todo_form_unchecked):
    model = todo_form_unchecked.to_model()
    assert model.completed is False


@pytest.mark.parametrize("value", ["off", "true", "yes", "", "0", "1", "random"])
def test_todo_form_to_model_completed_non_on(value):
    form = TodoForm(title="task", completed=value)
    model = form.to_model()
    assert model.completed is False
