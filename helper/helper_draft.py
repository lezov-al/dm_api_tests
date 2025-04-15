from json import loads


def get_activation_token_by_login(
        login,
        response
):
    """
    Get token from emailmessage
    :param login:
    :param response:
    :return:
    """
    token = None
    for message in response.json()['items']:
        user_data = loads(message['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            break

    return token
