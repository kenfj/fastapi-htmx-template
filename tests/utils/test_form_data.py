import io

from fastapi import UploadFile
from fastapi.datastructures import FormData

from utils.form_data import from_form_data


def test_from_form_data_str():
    form = FormData([("foo", "bar")])
    result = from_form_data(form)
    assert result == {"foo": "bar"}


def test_from_form_data_uploadfile():
    file = UploadFile(filename="test.txt", file=io.BytesIO(b"dummy"))
    form = FormData([("file", file)])
    result = from_form_data(form)
    assert result == {"file": ""}


def test_from_form_data_other():
    form = FormData([("num", "123")])
    result = from_form_data(form)
    assert result == {"num": "123"}
