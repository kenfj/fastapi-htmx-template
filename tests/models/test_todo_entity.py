from models import TodoEntity


def test_to_model_basic(basic_entity):
    model = basic_entity.to_model()

    assert model.title == "test"
    assert model.description == "desc"
    assert model.completed is True


def test_to_model_description_none(entity_with_none_description):
    model = entity_with_none_description.to_model()

    assert model.description == ""
    assert model.completed is False


def test_from_model_basic(basic_model):
    entity = TodoEntity.from_model(basic_model)

    assert entity.title == "test"
    assert entity.description == "desc"
    assert entity.completed is True


def test_from_model_description_empty_string(model_with_empty_description):
    entity = TodoEntity.from_model(model_with_empty_description)

    assert entity.description is None
    assert entity.completed is False
