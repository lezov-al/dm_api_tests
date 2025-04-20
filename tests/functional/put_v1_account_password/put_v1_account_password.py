def test_put_v1_account_password(
        account_helper,
        prepare_test_user

):
    login = prepare_test_user.login
    password = prepare_test_user.password
    email = prepare_test_user.email
    new_password = prepare_test_user.new_password

    account_helper.register_new_user(login=login, email=email, password=password)

    response = account_helper.auth_client(login=login, password=password)
    assert response.status_code == 200, f" Не удалось авторизовать пользователя {response.json()}"

    response = account_helper.change_password(
        login=login,
        email=email,
        old_password=password,
        new_password=new_password
    )
    assert response.status_code == 200, f" Не удалось изменить пароль {response.json()}"

    response = account_helper.user_login(login=login, password=new_password)
    assert response.status_code == 200, f" Не удалось авторизовать пользователя {response.json()}"
