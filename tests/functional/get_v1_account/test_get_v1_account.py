from checkers.http_checker import check_status_code_http
from checkers.get_v1_account import GetV1Account


def test_get_v1_account_no_auth(
        account_helper
):
    with check_status_code_http(401, 'User must be authenticated'):
        account_helper.get_current_user()


def test_get_v1_account_auth(
        auth_account_helper
):
    with check_status_code_http():
        response = auth_account_helper.get_current_user()
        login = response.resource.login
        GetV1Account.check_response_values(response, login)
