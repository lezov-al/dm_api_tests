from json import loads

import requests


class AccountApi:
    def __init__(
            self,
            host,
            headers=None
    ):
        self.host = host
        self.headers = headers

    def post_v1_account(
            self,
            json_data
    ):
        """
        Register new user
        :param json_data:
        :return:
        """
        response = requests.post(
            url=f'{self.host}/v1/account',
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
        response = requests.put(
            url=f'{self.host}/v1/account/{token}'
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

        response = requests.put(
            url=f'{self.host}/v1/account/email',
            json=json_data
        )

        return response
