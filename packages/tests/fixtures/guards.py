from typing import Optional
from unittest.mock import patch

import pytest
from getstanza.configuration import StanzaConfiguration
from getstanza.guard import Guard
from stanza.hub.v1 import common_pb2, config_pb2, quota_pb2_grpc
from tests.utils import async_noop, noop


def make_guard(
    quota_service: quota_pb2_grpc.QuotaServiceStub,
    stanza_config: StanzaConfiguration,
    guard_config: Optional[config_pb2.GuardConfig],
    guard_config_status: common_pb2.Config,
    guard_name: str,
    feature_name: Optional[str] = None,
    priority_boost: Optional[int] = None,
    default_weight: Optional[float] = None,
    tags=None,
):
    """Create a guard without starting any background tasks."""

    with (
        patch("getstanza.guard.batch_token_consumer_task") as batch_token_consumer_task,
        patch("getstanza.guard.batch_token_consumer") as batch_token_consumer,
        patch("getstanza.guard.handle_batch_token_consumer") as handle_batch_token_consumer,
    ):
        batch_token_consumer_task.return_value = async_noop
        batch_token_consumer.return_value = async_noop
        handle_batch_token_consumer.return_value = noop

        guard = Guard(
            quota_service,
            stanza_config,
            guard_config,
            guard_config_status,
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
def quota_guard(stanza_config, quota_guard_config, quota_service):
    return make_guard(
        quota_service,
        stanza_config,
        quota_guard_config,
        common_pb2.Config.CONFIG_CACHED_OK,
        "QuotaGuard",
        feature_name=None,
        priority_boost=0,
        tags=None,
    )


@pytest.fixture
def guard_without_config(stanza_config, quota_service):
    return make_guard(
        quota_service,
        stanza_config,
        None,
        common_pb2.Config.CONFIG_UNSPECIFIED,
        "GuardWithoutConfig",
        feature_name=None,
        priority_boost=0,
        tags=None,
    )


@pytest.fixture
def guard_without_config_fetch_error(stanza_config, quota_service):
    return make_guard(
        quota_service,
        stanza_config,
        None,
        common_pb2.Config.CONFIG_FETCH_ERROR,
        "GuardWithoutConfig",
        feature_name=None,
        priority_boost=0,
        tags=None,
    )


@pytest.fixture
def guard_without_config_fetch_timeout(stanza_config, quota_service):
    return make_guard(
        quota_service,
        stanza_config,
        None,
        common_pb2.Config.CONFIG_FETCH_TIMEOUT,
        "GuardWithoutConfig",
        feature_name=None,
        priority_boost=0,
        tags=None,
    )


@pytest.fixture
def guard_without_config_not_found(stanza_config, quota_service):
    return make_guard(
        quota_service,
        stanza_config,
        None,
        common_pb2.Config.CONFIG_NOT_FOUND,
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
def token_guard(stanza_config, quota_guard_config, quota_service):
    return make_guard(
        quota_service,
        stanza_config,
        quota_guard_config,
        common_pb2.Config.CONFIG_CACHED_OK,
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
def report_only_guard(stanza_config, report_only_guard_config, quota_service):
    return make_guard(
        quota_service,
        stanza_config,
        report_only_guard_config,
        common_pb2.Config.CONFIG_CACHED_OK,
        "ReportOnlyQuotaGuard",
        feature_name=None,
        priority_boost=0,
        tags=None,
    )


# TODO: Ingress token report only as well?