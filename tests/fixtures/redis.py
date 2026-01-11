import pytest


@pytest.fixture
def pubsub_mocks(mocker):
    """Mock redis and pubsub async context manager"""
    redis = mocker.AsyncMock()

    pubsub = mocker.AsyncMock()
    pubsub.__aenter__ = mocker.AsyncMock(return_value=pubsub)
    pubsub.__aexit__ = mocker.AsyncMock(return_value=None)
    pubsub.subscribe = mocker.AsyncMock()
    pubsub.get_message = mocker.AsyncMock()

    redis.pubsub = mocker.Mock(return_value=pubsub)
    return redis, pubsub
