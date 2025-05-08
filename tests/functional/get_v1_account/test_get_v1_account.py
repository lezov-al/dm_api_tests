import allure

from checkers.http_checker import check_status_code_http
from checkers.get_v1_account import GetV1Account


@allure.suite("Тесты на проверку метода GET v1/account")
class TestGetV1Account:
    @staticmethod
    @allure.title("Проверка получения данных неавторизованного пользователя")
    def test_get_v1_account_no_auth(
            account_helper
    ):
        with check_status_code_http(401, 'User must be authenticated'):
            account_helper.get_current_user()

    @staticmethod
    @allure.title("Проверка получения данных авторизованного пользователя")
    def test_get_v1_account_auth(
            auth_account_helper
    ):
        with check_status_code_http():
            response = auth_account_helper.get_current_user()
            login = response.resource.login
            GetV1Account.check_response_values(response, login)
