import allure


@allure.suite("Тесты на проверку метода Delete v1_account_login_all")
@allure.title("Проверка выхода со всех устройств")
def test_delete_v1_account_login_all(
        auth_account_helper
):
    auth_account_helper.user_logout_all()
