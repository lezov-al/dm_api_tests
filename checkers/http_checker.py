import requests
from contextlib import contextmanager
from requests.exceptions import HTTPError


@contextmanager
def check_status_code_http(
        expected_status_code: requests.codes = requests.codes.OK,
        expected_message: str = "",
):
    try:
        yield
        if expected_status_code != requests.codes.OK:
            raise AssertionError(f"Ожидаемый статус код должен быть = {expected_status_code}")
        if expected_message:
            raise AssertionError(f"Должно быть получено сообщение '{expected_message}', но запрос прошел успешно")

    except HTTPError as e:
        assert e.response.status_code == expected_status_code
        assert e.response.json()['title'] == expected_message


def check_field_error(
        response,
        field: str,
        message: str
):
    errors = response.json().get("errors", {})
    assert message in errors[field], f"Ожидалось сообщение '{message}' для поля '{field}'"
