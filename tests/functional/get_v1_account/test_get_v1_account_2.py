def test_get_v1_account_2(
        auth_account_helper

):
    """
    Тест для получения информации по захардкоженному пользователю
    """
    hard_code_user = auth_account_helper.get_current_user()
    print(hard_code_user)
    assert hard_code_user.status_code == 200, (f" Не удалось получить информацию о пользователе"
                                               f" {hard_code_user.json()}")
