from collections import namedtuple
from datetime import datetime
import pytest
from requests import HTTPError

from checkers.http_checker import (
    check_status_code_http,
    check_field_error,
)
from hamcrest import (
    assert_that,
    has_property,
    starts_with,
    all_of,
    instance_of,
    equal_to,
    has_properties,
)


def get_user_data():
    now = datetime.now()
    data = now.strftime("%d_%m_%Y_%H_%M_%S")

    login = f'test_negative{data}'
    email = f'{login}@mail.ru'
    password = '123123123'

    User = namedtuple("User", ['login', 'password', 'email'])
    user = User(login=login, password=password, email=email)
    return user


user_data = get_user_data()


@pytest.mark.parametrize(
    'login, password, email, field,  error_message', [
        (user_data.login, '123', user_data.email, 'Password', 'Short'),
        ('a', user_data.password, user_data.email, 'Login', 'Short'),
        (user_data.login, user_data.password, 'lolkek.ru', 'Email', 'Invalid'),
    ]
)
def test_post_v1_account_negative(
        login,
        password,
        email,
        field,
        error_message,
        account_helper,
        prepare_test_user,
):
    with check_status_code_http(
            expected_status_code=400,
            expected_message='Validation failed'
    ):
        response = account_helper.register_new_user(login=login, email=email, password=password)
        check_field_error(response.response, field, error_message)


def test_post_v1_account(
        account_helper,
        prepare_test_user
):
    login = prepare_test_user.login
    password = prepare_test_user.password
    email = prepare_test_user.email

    account_helper.register_new_user(login=login, email=email, password=password)
    response = account_helper.user_login(
        login=login,
        password=password,
        validate_response=True,
        validate_headers=False
    )

    assert_that(
        response, all_of(
            has_property('resource', has_property('login', starts_with("allezov"))),
            has_property('resource', has_property('registration', instance_of(datetime))),
            has_property(
                'resource', has_properties(
                    {
                        "rating": has_properties(
                            {
                                "enabled": equal_to(True),
                                "quality": equal_to(0),
                                "quantity": equal_to(0)
                            }
                        )
                    }
                )
            )
        )
    )
