import requests
import pprint
from json import loads


def test_post_v1_account():
    # Регистрация
    login = 'allezov2'
    email = f'{login}@mail.ru'
    password = '123123123'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account', json=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 201, f"Пользователь не был зарегистирован {response.json()}"

    # Получить письма из почтового сервера,
    params = {
        'limit': '50',
    }
    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params, verify=False)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, f" Письма не получены {response.json()}"

    # Получить активационный токен
    token = None
    for message in response.json()['items']:
        user_data = (loads(message['Content']['Body']))
        if user_data['Login'] == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
    assert token is not None, f"Токен для пользователя {login}, не был получен"

    # Активация
    response = requests.put(f'http://5.63.153.31:5051/v1/account/{token}')
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, f" Не удалось активировать пользователя {response.json()}"

    # Авторизация
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account/login', json=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, f" Не удалось авторизовать пользователя {response.json()}"
