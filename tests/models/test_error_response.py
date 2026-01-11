from models.error_response import ErrorResponse


class DummyError(Exception):
    pass


def test_from_exception_basic():
    msg = "dummy error"
    exc = DummyError(msg)
    response = ErrorResponse.from_exception(exc)

    assert response.error == "DummyError"
    assert response.detail == "dummy error"
    assert (
        response.trace == "tests.models.test_error_response.DummyError: dummy error\n"
    )


def _raise_dummy_error():
    msg = "trace test"
    raise DummyError(msg)


def test_from_exception_trace_content():
    try:
        _raise_dummy_error()
    except DummyError as exc:
        response = ErrorResponse.from_exception(exc)

        assert response.error == "DummyError"
        assert response.detail == "trace test"

        # Trace should contain exception type and message
        assert isinstance(response.trace, str)
        assert "DummyError" in response.trace
        assert "trace test" in response.trace
        # Should contain at least one 'File' line
        assert "File" in response.trace


def test_from_exception_with_builtin_exception():
    try:
        1 / 0  # noqa: B018  # type: ignore[division-by-zero]
    except ZeroDivisionError as exc:
        response = ErrorResponse.from_exception(exc)

        assert response.error == "ZeroDivisionError"
        assert response.detail == "division by zero"

        assert isinstance(response.trace, str)
        assert "ZeroDivisionError" in response.trace
        assert "division by zero" in response.trace
        assert "File" in response.trace
        assert "1 / 0" in response.trace
