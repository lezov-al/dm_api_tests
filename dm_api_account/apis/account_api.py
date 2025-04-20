from restclient.client import RestClient


class AccountApi(RestClient):
    def get_v1_account(
            self,
            **kwargs
    ):
        """
        Get current user
        :return:
        """
        response = self.get(
            path=f'/v1/account',
            **kwargs
        )

        return response

    def post_v1_account(
            self,
            json_data
    ):
        """
        Register new user
        :param json_data:
        :return:
        """
        response = self.post(
            path=f'/v1/account',
            json=json_data
        )

        return response

    def put_v1_account_token(
            self,
            token
    ):
        """
        Activate registered user
        :param token:
        :return:
        """
        response = self.put(
            path=f'/v1/account/{token}'
        )

        return response

    def put_v1_account_email(
            self,
            login,
            password,
            email
    ):
        """
        Change registered user email
        :param login:
        :param password:
        :param email:
        :return:
        """
        json_data = {
            'login': login,
            'password': password,
            'email': email
        }

        response = self.put(
            path=f'/v1/account/email',
            json=json_data
        )

        return response

    def put_v1_account_password(
            self,
            login,
            token,
            old_password,
            new_password
    ):
        """
        Change registered user password
        :param login:
        :param token:
        :param old_password:
        :param new_password:
        :return:
        """
        json_data = {
            'login': login,
            'token': token,
            'oldPassword': old_password,
            'newPassword': new_password,
        }

        response = self.put(
            path=f'/v1/account/password',
            json=json_data
        )

        return response

    def post_v1_account_password(
            self,
            login,
            email
    ):
        """
        Reset registered user password
        :param login:
        :param email:
        :return:
        """
        json_data = {
            'login': login,
            'email': email
        }

        response = self.post(
            path=f'/v1/account/password',
            json=json_data
        )

        return response
