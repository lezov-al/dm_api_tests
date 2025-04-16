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


def test_put_v1_account_email():
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)

    account = DmApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    # Регистрация
    login = f'mihailstena12'
    email = f'{login}@mail.ru'
    password = '123123123'
    new_email = email.replace('.ru', '.com')

    account_helper.register_new_user(login=login, email=email, password=password)
    account_helper.user_login(login=login, password=password)
    account_helper.change_user_email(login=login,password=password,new_email=new_email)
    account_helper.user_login_without_activation(login=login, email=email, password=password)
    account_helper.activate_user_email(login=login)
    account_helper.user_login(login=login, password=password)
