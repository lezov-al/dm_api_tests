def test_post_v1_account_login(
        account_helper,
        prepare_test_user
):
    login = prepare_test_user.login
    password = prepare_test_user.password
    email = prepare_test_user.email

    account_helper.register_new_user(login=login, email=email, password=password)
    account_helper.user_login(
        login=login,
        password=password,
        validate_response=True,
        validate_headers=False
    )
