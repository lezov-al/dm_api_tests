from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from helper import helper_draft


def test_post_v1_account():
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)

    account_api = AccountApi(dm_api_configuration)
    login_api = LoginApi(dm_api_configuration)
    mailhog_api = MailhogApi(mailhog_configuration)

    # Регистрация
    login = f'allezov17'
    email = f'{login}@mail.ru'
    password = '123123123'

    json_data = {
        'login': login,
        'email': email,
        'password': password
    }

    response = account_api.post_v1_account(json_data=json_data)
    assert response.status_code == 201, f"Пользователь не был зарегистирован {response.json()}"

    # Получить письма из почтового сервера
    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, f" Письма не получены {response.json()}"

    # Получить активационный токен
    token = helper_draft.get_activation_token_by_login(login=login, response=response)
    assert token is not None, f"Токен для пользователя {login}, не был получен"

    # Активация
    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, f" Не удалось активировать пользователя {response.json()}"

    # Авторизация
    response = login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 200, f" Не удалось авторизовать пользователя {response.json()}"
