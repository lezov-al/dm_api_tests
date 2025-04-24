from datetime import datetime

from checkers.http_checher import check_status_code_http
from dm_api_account.models.user_details_envelope import UserRole

from hamcrest import (
    assert_that,
    has_property,
    starts_with,
    all_of,
    instance_of,
    equal_to,
    has_properties,
    has_items,
)


def test_get_v1_account_no_auth(
        account_helper
):
    with check_status_code_http(401, 'User must be authenticated'):
        account_helper.get_current_user()


def test_get_v1_account_auth(
        auth_account_helper
):
    response = auth_account_helper.get_current_user()

    assert_that(
        response, all_of(
            has_property('resource', has_property('login', starts_with("allezov"))),
            has_property('resource', has_property('roles', has_items(UserRole.GUEST, UserRole.PLAYER))),
            has_property('resource', has_property('registration', instance_of(datetime))),
            has_property(
                'resource', has_properties(
                    {
                        "rating": has_properties(
                            {
                                "enabled": equal_to(True),
                                "quality": equal_to(0),
                                "quantity": equal_to(0)
                            }
                        )
                    }
                )
            )
        )
    )
