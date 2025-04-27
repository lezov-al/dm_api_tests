import requests
from contextlib import contextmanager
from requests.exceptions import HTTPError


@contextmanager
def check_status_code_http(
        expected_status_code: requests.codes = requests.codes.OK,
        expected_message: str = "",
        error_type: str = "",

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
        if error_type == 'email':
            assert e.response.json()['errors']['Email'][0] == 'Invalid'
        elif error_type == 'password':
            assert e.response.json()['errors']['Password'][0] == 'Short'
        elif error_type == 'login':
            assert e.response.json()['errors']['Login'][0] == 'Short'
