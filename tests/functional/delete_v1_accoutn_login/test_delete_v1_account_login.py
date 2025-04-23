def test_delete_v1_account_login(
        auth_account_helper
):
    response = auth_account_helper.user_logout()
    assert response.status_code == 204, f" Не удалось разлогинить пользователя {response.json()}"
