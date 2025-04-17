import time
from json import loads

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

        token = self.get_activation_token_by_login(login=login)
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
        return response

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

    @retrier
    def get_activation_token_by_login(
            self,
            login
    ):
        """
        Get token from emailmessage
        :param login:
        :param response:
        :return:
        """
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, f" Письма не получены {response.json()}"
        for message in response.json()['items']:
            user_data = loads(message['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                break

        return token
