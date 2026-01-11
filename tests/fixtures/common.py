from datetime import UTC, datetime

import pytest


@pytest.fixture
def fixed_datetime():
    return datetime(2025, 1, 1, 12, 0, 0, tzinfo=UTC)
