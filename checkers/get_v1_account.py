from datetime import datetime

from hamcrest import (
    assert_that,
    all_of,
    has_property,
    has_properties,
    equal_to,
    instance_of,
)


class GetV1Account:
    @staticmethod
    def check_response_values(
            response,
            login: str = ''
    ):
        assert_that(
            response, all_of(
                has_property('resource', has_property('login', equal_to(login))),
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
