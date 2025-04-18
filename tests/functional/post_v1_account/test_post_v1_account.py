from collections import namedtuple
from datetime import datetime

import pytest

from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from services.dm_api_account import DmApiAccount
from services.api_mailhog import MailHogApi
from helpers.account_helper import AccountHelper
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            sort_keys=True
        )
    ]
)


@pytest.fixture
def account_api():
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=True)
    account_client = DmApiAccount(configuration=dm_api_configuration)
    return account_client


@pytest.fixture
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    mailhog_client = MailHogApi(configuration=mailhog_configuration)
    return mailhog_client


@pytest.fixture()
def account_helper(
        account_api,
        mailhog_api
):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper


@pytest.fixture()
def prepare_test_user():
    now = datetime.now()
    data = now.strftime("%d_%m_%Y_%H_&M_%S")
    login = f'allezov{data}'
    email = f'{login}@mail.ru'
    password = '123123123'
    User = namedtuple("User", ['login', 'password', 'email'])
    user = User(login=login, password=password, email=email)
    return user


def test_post_v1_account(
        account_helper,
        prepare_test_user
):
    login = prepare_test_user.login
    password = prepare_test_user.password
    email = prepare_test_user.email

    account_helper.register_new_user(login=login, email=email, password=password)
    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 200, f" Не удалось авторизовать пользователя {response.json()}"
