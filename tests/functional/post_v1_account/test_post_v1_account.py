def test_post_v1_account(
        account_helper,
        prepare_test_user
):
    login = prepare_test_user.login
    password = prepare_test_user.password
    email = prepare_test_user.email

    account_helper.register_new_user(login=login, email=email, password=password)
    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 200, f" Не удалось авторизовать пользователя {response.json()}"
