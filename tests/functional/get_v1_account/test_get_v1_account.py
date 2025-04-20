def test_get_v1_account(
        account_helper,
        prepare_test_user

):
    """
    Тест для получения информации по пользователю, которого только что зарегестрировали.
    """
    login = prepare_test_user.login
    password = prepare_test_user.password
    email = prepare_test_user.email

    account_helper.register_new_user(login=login, email=email, password=password)

    response = account_helper.auth_client(login=login, password=password)
    assert response.status_code == 200, f" Не удалось авторизовать пользователя {response.json()}"

    current_user = account_helper.get_current_user()
    assert current_user.status_code == 200, (f" Не удалось получить информацию о пользователе {login},"
                                             f" {current_user.json()}")
