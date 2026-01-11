import pytest

from models import Todo, TodoEntity


@pytest.fixture
def basic_entity(fixed_datetime):
    return TodoEntity(
        id=1,
        title="test",
        description="desc",
        completed=True,
        created_at=fixed_datetime,
        updated_at=None,
    )


@pytest.fixture
def entity_with_none_description(fixed_datetime):
    return TodoEntity(
        id=2,
        title="test2",
        description=None,
        completed=False,
        created_at=fixed_datetime,
        updated_at=None,
    )


@pytest.fixture
def basic_model(fixed_datetime):
    return Todo(
        id=1,
        title="test",
        description="desc",
        completed=True,
        created_at=fixed_datetime,
        updated_at=None,
    )


@pytest.fixture
def model_with_empty_description(fixed_datetime):
    return Todo(
        id=4,
        title="test4",
        description="",
        completed=False,
        created_at=fixed_datetime,
        updated_at=None,
    )
