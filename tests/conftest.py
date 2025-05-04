from collections import namedtuple
from datetime import datetime

import pytest
from pathlib import Path
from vyper import v
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

options = (
    'service.dm_api_account',
    'service.mailhog',
    'user.login',
    'user.password',
)


@pytest.fixture(scope="session", autouse=True)
def set_config(
        request
        ):
    config = Path(__file__).joinpath("../../").joinpath("config")
    config_name = request.config.getoption("--env")
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()
    for option in options:
        v.set(f"{option}", request.config.getoption(f"--{option}"))


def pytest_addoption(
        parser
):
    parser.addoption("--env", action="store", default="stg", help="run stg")

    for option in options:
        parser.addoption(f"--{option}", action="store", default=None)


@pytest.fixture(scope='session')
def account_api():
    dm_api_configuration = DmApiConfiguration(host=v.get('service.dm_api_account'), disable_log=False)
    account_client = DmApiAccount(configuration=dm_api_configuration)
    return account_client


@pytest.fixture(scope='session')
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(host=v.get('service.mailhog'))
    mailhog_client = MailHogApi(configuration=mailhog_configuration)
    return mailhog_client


@pytest.fixture(scope='session')
def account_helper(
        account_api,
        mailhog_api
):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    yield account_helper
    account_helper.dm_api_account.close_session()


@pytest.fixture(scope='function')
def auth_account_helper(
        mailhog_api
):
    dm_api_configuration = DmApiConfiguration(host=v.get('service.dm_api_account'), disable_log=False)
    account_client = DmApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_account_api=account_client, mailhog=mailhog_api)

    account_helper.auth_client(
        login=v.get('user.login'),
        password=v.get('user.password'),
    )
    yield account_helper
    account_helper.dm_api_account.close_session()


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
