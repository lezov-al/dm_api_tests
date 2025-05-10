from packages.restclient.configuration import Configuration
from clients.http.dm_api_account.apis.account_api import AccountApi
from clients.http.dm_api_account.apis.login_api import LoginApi


class DmApiAccount:
    def __init__(
            self,
            configuration: Configuration
    ):
        self.configuration = configuration
        self.login_api = LoginApi(configuration=configuration)
        self.account_api = AccountApi(configuration=configuration)

    def close_session(
            self
    ):
        self.account_api.session.close()
        self.login_api.session.close()
