def test_put_v1_account_email(
        account_helper,
        prepare_test_user
):
    login = prepare_test_user.login
    password = prepare_test_user.password
    email = prepare_test_user.email
    new_email = prepare_test_user.new_email

    account_helper.register_new_user(login=login, email=email, password=password)

    account_helper.user_login(login=login, password=password)

    account_helper.change_user_email(login=login, password=password, new_email=new_email)

    account_helper.user_login(login=login, password=password,validate_response=False)

    account_helper.activate_user(login=login)

    account_helper.user_login(login=login, password=password)
