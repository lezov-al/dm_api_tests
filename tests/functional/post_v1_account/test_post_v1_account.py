from collections import namedtuple
from datetime import datetime

import allure
import pytest
from checkers.post_v1_account import PostV1Account
from checkers.http_checker import (
    check_status_code_http,
    check_field_error,
)


@allure.suite("Тесты на проверку метода POST v1/account")
class TestPostV1Account:
    @staticmethod
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

    @staticmethod
    @allure.title("Валидация некорректных данных при регистрации")
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

    @staticmethod
    @allure.title("Проверка регистрации нового пользователя")
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
        checker_login = login.split('_')[0]
        PostV1Account.check_response_values(response, login=checker_login)
