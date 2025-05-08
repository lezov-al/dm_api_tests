import allure


@allure.suite("Тесты на проверку метода Delete v1_account_login")
@allure.title("Проверка выхода с одного устройства")
def test_delete_v1_account_login(
        auth_account_helper
):
    auth_account_helper.user_logout()
