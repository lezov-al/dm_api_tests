def test_put_v1_account_token(
        account_helper,
        prepare_test_user
):
    login = prepare_test_user.login
    password = prepare_test_user.password
    email = prepare_test_user.email

    account_helper.register_new_user(login=login, email=email, password=password)
    account_helper.user_login(login=login, password=password)
