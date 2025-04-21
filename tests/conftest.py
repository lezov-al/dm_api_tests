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


@pytest.fixture(scope='session')
def account_api():
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=True)
    account_client = DmApiAccount(configuration=dm_api_configuration)
    return account_client


@pytest.fixture(scope='session')
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    mailhog_client = MailHogApi(configuration=mailhog_configuration)
    return mailhog_client


@pytest.fixture(scope='session')
def account_helper(
        account_api,
        mailhog_api
):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper


@pytest.fixture(scope='function')
def auth_account_helper(
        mailhog_api,
        prepare_test_user
):
    print('prepare_test_user_fixture', prepare_test_user)
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=True)
    account_client = DmApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_account_api=account_client, mailhog=mailhog_api)
    account_helper.auth_client(login='allezov99', password='123123123')
    # draft
    # account_helper.auth_client(login=prepare_test_user.login, password=prepare_test_user.password)
    return account_helper


@pytest.fixture
def prepare_test_user():
    now = datetime.now()
    data = now.strftime("%d_%m_%Y_%H_%M_%S")

    login = f'allezov_{data}'
    email = f'{login}@mail.ru'
    new_email = email.replace('.ru', '.com')
    password = '123123123'
    new_password = '321321321'

    User = namedtuple("User", ['login', 'password', 'email', 'new_email', 'new_password'])
    user = User(login=login, password=password, email=email, new_email=new_email, new_password=new_password)
    return user
