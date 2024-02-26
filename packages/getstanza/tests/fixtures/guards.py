from collections import defaultdict
from typing import Optional
from unittest.mock import patch

import pytest
from getstanza import guard
from getstanza.guard import Guard
from getstanza.hub import StanzaHub
from getstanza.propagation import context_from_http_headers
from getstanza.tests.utils import async_noop, async_return, noop
from pytest_socket import enable_socket, socket_allow_hosts
from stanza.hub.v1 import common_pb2, config_pb2


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Clear global cached and consumed lease state between each test."""

    # Block internet access by default for all tests as we mock all calls going
    # out to Hub. Tests will throw 'SocketBlockedError' errors if a mock is
    # missing whilst executing them.
    #
    # We have two notable exceptions. We explicitly allow localhost so that the
    # VSCode debugger doesn't get blocked, and we also allow UNIX sockets since
    # asyncio appears to rely on them.
    socket_allow_hosts(allowed=["localhost"], allow_unix_socket=True)

    # Initialize an empty context for the tests. If we don't do this then we'll
    # get LookupError errors as these tests don't check for incoming baggage.
    context_from_http_headers({})

    yield  # Run the test before executing the teardown logic.

    with guard.cached_leases_lock:
        guard.cached_leases = defaultdict(list)

    with guard.consumed_leases_lock:
        guard.consumed_leases = defaultdict(list)

    enable_socket()


def make_guard(
    hub: StanzaHub,
    guard_name: str,
    feature_name: Optional[str] = None,
    priority_boost: Optional[int] = None,
    default_weight: Optional[float] = None,
    tags=None,
):
    """Create a guard without starting any background tasks."""

    with (
        patch(
            "getstanza.guard.batch_token_consumer_handle"
        ) as batch_token_consumer_handle,
        patch("getstanza.guard.batch_token_consumer") as batch_token_consumer,
        patch(
            "getstanza.guard.handle_batch_token_consumer"
        ) as handle_batch_token_consumer,
    ):
        batch_token_consumer_handle.return_value = async_noop
        batch_token_consumer.return_value = async_noop
        handle_batch_token_consumer.return_value = noop

        guard = Guard(
            hub,
            guard_name,
            feature_name=feature_name,
            priority_boost=priority_boost,
            default_weight=default_weight,
            tags=tags,
        )

        return guard


@pytest.fixture
def quota_guard_config():
    return config_pb2.GuardConfig(
        validate_ingress_tokens=False,
        check_quota=True,
        quota_tags=[],
        report_only=False,
    )


@pytest.fixture
def quota_guard(stanza_hub, quota_guard_config):
    stanza_hub.config_manager.get_guard_config.return_value = async_return(
        (quota_guard_config, common_pb2.Config.CONFIG_CACHED_OK)
    )
    return make_guard(
        stanza_hub,
        "QuotaGuard",
        feature_name=None,
        priority_boost=0,
        tags=None,
    )


@pytest.fixture
def quota_guard_with_feature(stanza_hub, quota_guard_config):
    stanza_hub.config_manager.get_guard_config.return_value = async_return(
        (quota_guard_config, common_pb2.Config.CONFIG_CACHED_OK)
    )
    return make_guard(
        stanza_hub,
        "QuotaGuard",
        feature_name="QuotaGuardFeature",
        priority_boost=0,
        tags=None,
    )


@pytest.fixture
def quota_guard_with_priority_boost(stanza_hub, quota_guard_config):
    stanza_hub.config_manager.get_guard_config.return_value = async_return(
        (quota_guard_config, common_pb2.Config.CONFIG_CACHED_OK)
    )
    return make_guard(
        stanza_hub,
        "QuotaGuard",
        feature_name=None,
        priority_boost=5,
        tags=None,
    )


@pytest.fixture
def guard_without_config(stanza_hub):
    stanza_hub.config_manager.get_guard_config.return_value = async_return(
        (None, common_pb2.Config.CONFIG_UNSPECIFIED)
    )
    return make_guard(
        stanza_hub,
        "GuardWithoutConfig",
        feature_name=None,
        priority_boost=0,
        tags=None,
    )


@pytest.fixture
def guard_without_config_fetch_error(stanza_hub):
    stanza_hub.config_manager.get_guard_config.return_value = async_return(
        (None, common_pb2.Config.CONFIG_FETCH_ERROR)
    )
    return make_guard(
        stanza_hub,
        "GuardWithoutConfig",
        feature_name=None,
        priority_boost=0,
        tags=None,
    )


@pytest.fixture
def guard_without_config_fetch_timeout(stanza_hub):
    stanza_hub.config_manager.get_guard_config.return_value = async_return(
        (None, common_pb2.Config.CONFIG_FETCH_TIMEOUT)
    )
    return make_guard(
        stanza_hub,
        "GuardWithoutConfig",
        feature_name=None,
        priority_boost=0,
        tags=None,
    )


@pytest.fixture
def guard_without_config_not_found(stanza_hub):
    stanza_hub.config_manager.get_guard_config.return_value = async_return(
        (None, common_pb2.Config.CONFIG_NOT_FOUND)
    )
    return make_guard(
        stanza_hub,
        "GuardWithoutConfig",
        feature_name=None,
        priority_boost=0,
        tags=None,
    )


@pytest.fixture
def token_guard_config():
    return config_pb2.GuardConfig(
        validate_ingress_tokens=True,
        check_quota=False,
        quota_tags=[],
        report_only=False,
    )


@pytest.fixture
def token_guard(stanza_hub, token_guard_config):
    stanza_hub.config_manager.get_guard_config.return_value = async_return(
        (token_guard_config, common_pb2.Config.CONFIG_CACHED_OK)
    )
    return make_guard(
        stanza_hub,
        "TokenGuard",
        feature_name=None,
        priority_boost=0,
        tags=None,
    )


@pytest.fixture
def report_only_guard_config():
    return config_pb2.GuardConfig(
        validate_ingress_tokens=False,
        check_quota=True,
        quota_tags=[],
        report_only=True,
    )


@pytest.fixture
def report_only_guard(stanza_hub, report_only_guard_config):
    stanza_hub.config_manager.get_guard_config.return_value = async_return(
        (report_only_guard_config, common_pb2.Config.CONFIG_CACHED_OK)
    )
    return make_guard(
        stanza_hub,
        "ReportOnlyQuotaGuard",
        feature_name=None,
        priority_boost=0,
        tags=None,
    )


# TODO: Ingress token report only as well?
