def test_get_v1_account(
        auth_account_helper
):
    current_user = auth_account_helper.get_current_user()
    assert current_user.status_code == 200, (f" Не удалось получить информацию о пользователе"
                                             f" {current_user.json()}")
