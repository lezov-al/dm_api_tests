import allure

from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient


class LoginApi(RestClient):
    @allure.step("Аутентификация пользователя")
    def post_v1_account_login(
            self,
            validate_response,
            login_credentials: LoginCredentials
    ):
        """
        Authenticate via credentials
        :param login_credentials
        :param validate_response
        :return:
        """
        response = self.post(
            path=f'/v1/account/login',
            json=login_credentials.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
            return UserEnvelope(**response.json())

        return response

    @allure.step("Logout пользователя с текущего устройства")
    def delete_v1_account_login(
            self
    ):
        """
        Logout as current user
        :return:
        """
        response = self.delete(
            path=f'/v1/account/login'
        )

        return response

    @allure.step("Logout пользователя со всех устройств")
    def delete_v1_account_login_all(
            self
    ):
        """
        Logout from every device
        :return:
        """
        response = self.delete(
            path=f'/v1/account/login/all',
        )

        return response
