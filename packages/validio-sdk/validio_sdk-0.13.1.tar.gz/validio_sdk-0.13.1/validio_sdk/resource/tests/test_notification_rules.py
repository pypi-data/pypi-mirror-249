import pytest

from validio_sdk.resource._resource import ResourceGraph
from validio_sdk.resource.channels import SlackChannel
from validio_sdk.resource.credentials import DemoCredential
from validio_sdk.resource.notification_rules import (
    Conditions,
    NotificationRule,
    NotificationTypename,
)
from validio_sdk.resource.sources import DemoSource, Source


@pytest.mark.parametrize(
    ("sources", "notification_typenames", "conditions", "should_raise"),
    [
        (
            None,
            [NotificationTypename.SegmentLimitExceededNotification],
            Conditions(),
            True,
        ),
        (
            [
                DemoSource(
                    name="demo_source",
                    credential=DemoCredential(
                        name="demo_credential", __internal__=ResourceGraph()
                    ),
                )
            ],
            None,
            Conditions(),
            True,
        ),
        (
            [
                DemoSource(
                    name="demo_source",
                    credential=DemoCredential(
                        name="demo_credential", __internal__=ResourceGraph()
                    ),
                )
            ],
            [NotificationTypename.SegmentLimitExceededNotification],
            None,
            False,
        ),
        (None, None, None, False),
    ],
)
def test_condition_permutation(
    sources: list[Source] | None,
    notification_typenames: list[NotificationTypename] | None,
    conditions: Conditions | None,
    should_raise: bool,
) -> None:
    ch = SlackChannel(
        __internal__=ResourceGraph(),
        name="my-channel",
        application_link_url="http://app.url",
        webhook_url="http://webhook.url",
    )

    got_exception = None
    did_raise = False
    try:
        NotificationRule(
            name="unit_test",
            channel=ch,
            sources=sources,
            notification_typenames=notification_typenames,
            conditions=conditions,
        )
    except Exception as e:
        got_exception = e
        did_raise = True

    if not should_raise and got_exception:
        print("expected no exception but got one:")
        print(got_exception)

    assert did_raise == should_raise
