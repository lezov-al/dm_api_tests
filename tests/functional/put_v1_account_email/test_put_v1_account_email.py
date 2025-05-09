import allure

from checkers.http_checker import check_status_code_http


@allure.suite("Тесты на проверку метода PUT v1_account_email")
@allure.title("Проверка смены почтового адреса")
def test_put_v1_account_email(
        account_helper,
        prepare_test_user
):
    login = prepare_test_user.login
    password = prepare_test_user.password
    email = prepare_test_user.email
    new_email = prepare_test_user.new_email

    account_helper.register_new_user(login=login, email=email, password=password)

    with check_status_code_http(200):
        account_helper.user_login(
            login=login,
            password=password,
            validate_response=True,
            validate_headers=False
        )

    account_helper.change_user_email(login=login, password=password, new_email=new_email)

    with check_status_code_http(403, 'User is inactive. Address the technical support for more details'):
        account_helper.user_login(
            login=login,
            password=password,
            validate_response=True,
            validate_headers=False
        )

    account_helper.activate_user(login=login)

    with check_status_code_http(200):
        account_helper.user_login(
            login=login,
            password=password,
            validate_response=True,
            validate_headers=False
        )
