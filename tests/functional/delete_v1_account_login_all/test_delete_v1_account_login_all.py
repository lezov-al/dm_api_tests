def test_delete_v1_account_login_all(
        prepare_test_user,
        account_helper
):
    login = prepare_test_user.login
    password = prepare_test_user.password
    email = prepare_test_user.email

    account_helper.register_new_user(login=login, email=email, password=password)

    response = account_helper.auth_client(login=login, password=password)
    assert response.status_code == 200, f" Не удалось авторизовать пользователя {response.json()}"

    response = account_helper.user_logout_all()
    assert response.status_code == 204, f" Не удалось разлогинить пользователя со всех устройств {response.json()}"
