import time
from json import loads

from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.registration import Registration
from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.reset_password import ResetPassword
from services.api_mailhog import MailHogApi
from services.dm_api_account import DmApiAccount


def retrier(
        func
):
    def wrapper(
            *args,
            **kwargs
    ):
        token = None
        count = 0
        while token is None:
            print(f"Попытка получения токена номер {count + 1}")
            token = func(*args, **kwargs)
            count += 1
            if count == 5:
                raise AssertionError("Превышено кол-во попыток получения активационного токена")
            if token:
                return token
            time.sleep(1)

    return wrapper


class AccountHelper:
    def __init__(
            self,
            dm_account_api: DmApiAccount,
            mailhog: MailHogApi
    ):
        self.dm_api_account = dm_account_api
        self.mailhog = mailhog

    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):
        registration = Registration(
            login=login,
            password=password,
            email=email
        )

        response = self.dm_api_account.account_api.post_v1_account(registration=registration)
        assert response.status_code == 201, f"Пользователь не был зарегистирован {response.json()}"

        response = self.activate_user_email(login=login)
        return response

    def activate_user_email(
            self,
            login: str
    ):
        start_time = time.time()
        token = self.get_activation_token_by_login(login=login)
        end_time = time.time()
        assert end_time - start_time < 3, "Время ожидания активации превышено"
        assert token is not None, f"Токен для пользователя {login}, не был получен"

        return self.dm_api_account.account_api.put_v1_account_token(token=token)

    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
            validate_response: bool = False,
            validate_headers: bool = False
    ):
        login_credentials = LoginCredentials(
            login=login,
            password=password,
            rememberMe=remember_me
        )
        response = self.dm_api_account.login_api.post_v1_account_login(
            login_credentials=login_credentials,
            validate_response=validate_response
        )
        if validate_headers:
            assert response.headers["x-dm-auth-token"], "Токен для пользователя не был получен"
            assert response.status_code == 200, "Пользователь не смог авторизоваться"

        return response

    def user_logout(
            self
    ):
        response = self.dm_api_account.login_api.delete_v1_account_login()

        return response

    def user_logout_all(
            self
    ):
        response = self.dm_api_account.login_api.delete_v1_account_login_all()

        return response

    def change_user_email(
            self,
            login: str,
            password: str,
            new_email: str
    ):
        change_email = ChangeEmail(
            login=login,
            password=password,
            email=new_email
        )

        self.dm_api_account.account_api.put_v1_account_email(change_email=change_email)

    def get_current_user(
            self
    ):
        response = self.dm_api_account.account_api.get_v1_account()
        return response

    def auth_client(
            self,
            login: str,
            password: str,
            email: str
    ):
        self.register_new_user(login=login, password=password, email=email)

        response = self.user_login(login=login, password=password)
        token = {
            "x-dm-auth-token": response.headers["x-dm-auth-token"]
        }
        self.dm_api_account.account_api.set_headers(token)
        self.dm_api_account.login_api.set_headers(token)

        return response

    @retrier
    def get_activation_token_by_login(
            self,
            login: str
    ):
        """
        Get token from email message
        :param login:
        :return:
        """
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, f" Письма не получены {response.json()}"
        for message in response.json()['items']:
            user_data = loads(message['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token_info = user_data.get('ConfirmationLinkUrl') or user_data.get('ConfirmationLinkUri')
                token = token_info.split('/')[-1]
                break

        return token

    def change_password(
            self,
            login: str,
            email: str,
            old_password: str,
            new_password: str,
    ):
        reset_password = ResetPassword(
            login=login,
            email=email
        )
        response = self.dm_api_account.account_api.post_v1_account_password(reset_password=reset_password)
        assert response.status_code == 200, f" Не удалось сбросил пароль, {response.json()}"

        token = self.get_activation_token_by_login(login=login)

        change_password = ChangePassword(
            login=login,
            token=token,
            newPassword=new_password,
            oldPassword=old_password

        )
        response = self.dm_api_account.account_api.put_v1_account_password(
            change_password=change_password
        )

        return response
