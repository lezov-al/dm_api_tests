def test_put_v1_account_password(
        auth_account_helper,
        prepare_test_user

):
    login = prepare_test_user.login
    password = prepare_test_user.password
    email = prepare_test_user.email
    new_password = prepare_test_user.new_password

    response = auth_account_helper.change_password(
        login=login,
        email=email,
        old_password=password,
        new_password=new_password
    )
    assert response.status_code == 200, f" Не удалось изменить пароль {response.json()}"

    response = auth_account_helper.user_login(login=login, password=new_password)
    assert response.status_code == 200, f" Не удалось авторизовать пользователя {response.json()}"
