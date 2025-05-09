import allure

from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from dm_api_account.models.user_details_envelope import UserDetailsEnvelope
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient


class AccountApi(RestClient):
    @allure.step("Получить информацию по текущему пользователю")
    def get_v1_account(
            self,
            validate_response=True,
            **kwargs
    ):
        """
        Get current user
        :return:
        """
        response = self.get(
            path=f'/v1/account',
            **kwargs
        )

        if validate_response:
            return UserDetailsEnvelope(**response.json())

        return response

    @allure.step("Регистрация нового пользователя")
    def post_v1_account(
            self,
            registration: Registration
    ):
        """
        Register new user
        :return:
        """
        response = self.post(
            path=f'/v1/account',
            json=registration.model_dump(exclude_none=True, by_alias=True)
        )

        return response

    @allure.step("Активация пользователя")
    def put_v1_account_token(
            self,
            token,
            validate_response=True
    ):
        """
        Activate registered user
        :param token:
        :param validate_response:
        :return:
        """
        response = self.put(
            path=f'/v1/account/{token}'
        )
        if validate_response:
            return UserEnvelope(**response.json())

        return response

    @allure.step("Изменить email пользователя")
    def put_v1_account_email(
            self,
            change_email: ChangeEmail,
            validate_response=True
    ):
        """
        Change registered user email
        :param change_email:
        :param validate_response:
        :return:
        """

        response = self.put(
            path=f'/v1/account/email',
            json=change_email.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
            return UserDetailsEnvelope(**response.json())
        return response

    @allure.step("Изменить password пользователя")
    def put_v1_account_password(
            self,
            change_password: ChangePassword,
            validate_response=False
    ):
        """
        Change registered user password
        :param change_password:
        :param validate_response:
        :return:
        """
        response = self.put(
            path=f'/v1/account/password',
            json=change_password.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
            return UserEnvelope(**response.json())

        return response

    @allure.step("Сбросить password пользователя")
    def post_v1_account_password(
            self,
            reset_password: ResetPassword
    ):
        """
        Reset registered user password
        :param reset_password:
        :return:
        """

        response = self.post(
            path=f'/v1/account/password',
            json=reset_password.model_dump(exclude_none=True, by_alias=True)
        )

        return response
