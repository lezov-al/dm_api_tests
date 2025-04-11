from json import loads

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi


def test_put_v1_account_token():
    account_api = AccountApi(host='http://5.63.153.31:5051')
    login_api = LoginApi(host='http://5.63.153.31:5051')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025')

    # Регистрация
    login = f'kol9n_iz_dvora3'
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
    token = get_activation_token_by_login(login=login, response=response)
    assert token is not None, f"Токен для пользователя {login}, не был получен"

    # Активация
    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, f" Не удалось активировать пользователя {response.json()}"

    # Авторизация
    response = login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 200, f" Не удалось авторизовать пользователя {response.json()}"


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

    return token
