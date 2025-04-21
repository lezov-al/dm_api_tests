def test_delete_v1_account_login(
        prepare_test_user,
        auth_account_helper
):
    print(prepare_test_user, 'prepare_test_user')  # login='allezov_21_04_2025_13_44_41
    login = prepare_test_user.login
    password = prepare_test_user.password
    email = prepare_test_user.email

    auth_account_helper.register_new_user(login=login, email=email, password=password)

    current_user = auth_account_helper.get_current_user()
    print(current_user.json())  # 'login': 'allezov99'

    response = auth_account_helper.user_logout()
    assert response.status_code == 204, f" Не удалось разлогинить пользователя {response.json()}"
