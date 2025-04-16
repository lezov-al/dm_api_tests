from json import loads

from services.api_mailhog import MailHogApi
from services.dm_api_account import DmApiAccount


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
        json_data = {
            'login': login,
            'email': email,
            'password': password
        }

        response = self.dm_api_account.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f"Пользователь не был зарегистирован {response.json()}"

        self.activate_user_email(login=login)

        response = self.dm_api_account.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 200, f" Не удалось авторизовать пользователя {response.json()}"

    def activate_user_email(
            self,
            login: str
    ):
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, f" Письма не получены {response.json()}"

        token = self.get_activation_token_by_login(login=login, response=response)
        assert token is not None, f"Токен для пользователя {login}, не был получен"

        response = self.dm_api_account.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, f" Не удалось активировать пользователя {response.json()}"

    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True
    ):
        json_data = {
            'login': login,
            'password': password,
            'remember_me': remember_me
        }

        response = self.dm_api_account.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 200, f" Не удалось авторизовать пользователя {response.json()}"
        return response

    def user_login_without_activation(
            self,
            login: str,
            password: str,
            email: str
    ):

        json_data = {
            'login': login,
            'email': email,
            'password': password
        }
        response = self.dm_api_account.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 403, (f"Ожидался статус 403 (Forbidden), но получен {response.status_code},"
                                             f" {response.json()}")

    def change_user_email(
            self,
            login: str,
            password: str,
            new_email: str
    ):

        response = self.dm_api_account.account_api.put_v1_account_email(
            login=login,
            password=password,
            email=new_email
        )

        assert response.status_code == 200, f" Не удалось изменить email пользователю {login}, {response.json()}"

    @staticmethod
    def get_activation_token_by_login(
            login,
            response
    ):
        """
        Get token from emailmessage
        :param login:
        :param response:
        :return:
        """
        token = None
        for message in response.json()['items']:
            user_data = loads(message['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                break

        return token
