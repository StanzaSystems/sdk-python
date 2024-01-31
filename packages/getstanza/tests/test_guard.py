from collections import defaultdict

import pytest
from getstanza import guard
from getstanza.propagation import context_from_http_headers
from pytest_socket import enable_socket, socket_allow_hosts
from stanza.hub.v1 import quota_pb2
from stanza.hub.v1.common_pb2 import Local, Quota, Token


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


def test_guard_allows_default(quota_guard):
    """Check that an unevaluated guard does not block by default."""

    assert quota_guard.guard_config is None
    assert quota_guard.allowed()


@pytest.mark.asyncio
async def test_guard_allows_when_config_null(quota_service, guard_without_config):
    """It should allow if getting the configuration fails (config is null)"""

    await guard_without_config.run()

    quota_service.GetTokenLease.assert_not_called()
    assert guard_without_config.local_status == Local.LOCAL_NOT_EVAL
    assert guard_without_config.token_status == Token.TOKEN_NOT_EVAL
    assert guard_without_config.quota_status == Quota.QUOTA_NOT_EVAL
    assert guard_without_config.error is not None
    assert guard_without_config.allowed()


@pytest.mark.asyncio
async def test_guard_allows_when_config_fetch_error(
    quota_service, guard_without_config_fetch_error
):
    """It should allow if getting the configuration fails (fetch error)"""

    await guard_without_config_fetch_error.run()

    quota_service.GetTokenLease.assert_not_called()
    assert guard_without_config_fetch_error.local_status == Local.LOCAL_NOT_EVAL
    assert guard_without_config_fetch_error.token_status == Token.TOKEN_NOT_EVAL
    assert guard_without_config_fetch_error.quota_status == Quota.QUOTA_NOT_EVAL
    assert guard_without_config_fetch_error.allowed()


@pytest.mark.asyncio
async def test_guard_allows_when_config_fetch_timeout(
    quota_service, guard_without_config_fetch_timeout
):
    """It should allow if getting the configuration fails (fetch timeout)"""

    await guard_without_config_fetch_timeout.run()

    quota_service.GetTokenLease.assert_not_called()
    assert guard_without_config_fetch_timeout.local_status == Local.LOCAL_NOT_EVAL
    assert guard_without_config_fetch_timeout.token_status == Token.TOKEN_NOT_EVAL
    assert guard_without_config_fetch_timeout.quota_status == Quota.QUOTA_NOT_EVAL
    assert guard_without_config_fetch_timeout.allowed()


@pytest.mark.asyncio
async def test_guard_blocks_when_config_not_found(
    quota_service, guard_without_config_not_found
):
    """It should block if getting the configuration fails (not found)"""

    await guard_without_config_not_found.run()

    quota_service.GetTokenLease.assert_not_called()
    assert guard_without_config_not_found.local_status == Local.LOCAL_NOT_EVAL
    assert guard_without_config_not_found.token_status == Token.TOKEN_NOT_EVAL
    assert guard_without_config_not_found.quota_status == Quota.QUOTA_NOT_EVAL
    assert guard_without_config_not_found.blocked()


# ===================
# === Quota Tests ===
# ===================


@pytest.mark.asyncio
async def test_guard_quota_end(quota_guard):
    await quota_guard.run()
    quota_guard.end(0)
    quota_guard.end(quota_guard.success)
    quota_guard.end(quota_guard.failure)


@pytest.mark.asyncio
async def test_guard_quota_allowed(quota_guard, quota_service):
    """Check that quota allowing works in a simple use case."""

    quota_service.GetTokenLease.return_value = quota_pb2.GetTokenLeaseResponse(
        granted=True,
        leases=[
            quota_pb2.TokenLease(
                duration_msec=86400,
                token="00000000",
                feature=None,
                priority_boost=0,
                weight=None,
                reason=None,
                expires_at=None,
                mode=None,
            )
        ],
    )

    await quota_guard.run()
    quota_guard.end(quota_guard.success)

    quota_service.GetTokenLease.assert_called_once()
    assert quota_guard.local_status == Local.LOCAL_NOT_SUPPORTED
    assert quota_guard.token_status == Token.TOKEN_EVAL_DISABLED
    assert quota_guard.quota_status == Quota.QUOTA_GRANTED
    assert quota_guard.quota_token is not None
    assert quota_guard.block_message is None
    assert quota_guard.block_reason is None
    assert quota_guard.allowed()


@pytest.mark.asyncio
async def test_guard_quota_blocked(quota_guard, quota_service):
    """Check that quota blocking works in a simple use case."""

    quota_service.GetTokenLease.return_value = quota_pb2.GetTokenLeaseResponse(
        granted=False,
        leases=[],
    )

    await quota_guard.run()

    quota_service.GetTokenLease.assert_called_once()
    assert quota_guard.local_status == Local.LOCAL_NOT_SUPPORTED
    assert quota_guard.token_status == Token.TOKEN_EVAL_DISABLED
    assert quota_guard.quota_status == Quota.QUOTA_BLOCKED
    assert (
        quota_guard.block_message == "Stanza quota exhausted. Please try again later."
    )
    assert quota_guard.block_reason == "QUOTA_BLOCKED"
    assert quota_guard.blocked()


@pytest.mark.asyncio
async def test_guard_feature_passed(quota_guard_with_feature, quota_service):
    """It should request quota with specified feature."""

    quota_service.GetTokenLease.return_value = quota_pb2.GetTokenLeaseResponse(
        granted=False,
        leases=[],
    )

    await quota_guard_with_feature.run()

    quota_service.GetTokenLease.assert_called_once()

    token_lease_request: quota_pb2.GetTokenLeaseRequest = (
        quota_service.GetTokenLease.call_args.kwargs["request"]
    )
    assert token_lease_request.selector.feature_name == "QuotaGuardFeature"

    assert quota_guard_with_feature.local_status == Local.LOCAL_NOT_SUPPORTED
    assert quota_guard_with_feature.token_status == Token.TOKEN_EVAL_DISABLED
    assert quota_guard_with_feature.quota_status == Quota.QUOTA_BLOCKED
    assert quota_guard_with_feature.blocked()


@pytest.mark.asyncio
async def test_guard_priority_boost_passed(
    quota_guard_with_priority_boost, quota_service
):
    """It should request quota with specified priority boost."""

    quota_service.GetTokenLease.return_value = quota_pb2.GetTokenLeaseResponse(
        granted=False,
        leases=[],
    )

    await quota_guard_with_priority_boost.run()

    quota_service.GetTokenLease.assert_called_once()

    token_lease_request: quota_pb2.GetTokenLeaseRequest = (
        quota_service.GetTokenLease.call_args.kwargs["request"]
    )
    assert token_lease_request.priority_boost == 5

    assert quota_guard_with_priority_boost.local_status == Local.LOCAL_NOT_SUPPORTED
    assert quota_guard_with_priority_boost.token_status == Token.TOKEN_EVAL_DISABLED
    assert quota_guard_with_priority_boost.quota_status == Quota.QUOTA_BLOCKED
    assert quota_guard_with_priority_boost.blocked()


# TODO: Add baggage and context tests


# ===========================
# === Ingress Token Tests ===
# ===========================


@pytest.mark.asyncio
async def test_guard_valid_ingress_token(token_guard, quota_service):
    """It should validate token before proceeding with execution."""

    quota_service.ValidateToken.return_value = quota_pb2.ValidateTokenResponse(
        valid=True,
        tokens_valid=[],
    )

    await token_guard.run(tokens=["valid_token"])

    quota_service.GetTokenLease.assert_not_called()
    quota_service.ValidateToken.assert_called_once()

    assert token_guard.local_status == Local.LOCAL_NOT_SUPPORTED
    assert token_guard.token_status == Token.TOKEN_VALID
    assert token_guard.quota_status == Quota.QUOTA_EVAL_DISABLED
    assert token_guard.allowed()


@pytest.mark.asyncio
async def test_guard_invalid_ingress_token(token_guard, quota_service):
    """It should block invalid tokens before proceeding with execution."""

    quota_service.ValidateToken.return_value = quota_pb2.ValidateTokenResponse(
        valid=False,
        tokens_valid=[],
    )

    await token_guard.run(tokens=["invalid_token"])

    quota_service.GetTokenLease.assert_not_called()
    quota_service.ValidateToken.assert_called_once()

    assert token_guard.local_status == Local.LOCAL_NOT_SUPPORTED
    assert token_guard.token_status == Token.TOKEN_NOT_VALID
    assert token_guard.quota_status == Quota.QUOTA_NOT_EVAL
    assert token_guard.block_message == "Invalid or expired X-Stanza-Token."
    assert token_guard.block_reason == "TOKEN_NOT_VALID"
    assert token_guard.blocked()


@pytest.mark.asyncio
async def test_guard_missing_ingress_token(token_guard, quota_service):
    """It should block missing token before proceeding with execution."""

    await token_guard.run()

    quota_service.GetTokenLease.assert_not_called()
    quota_service.ValidateToken.assert_not_called()

    assert token_guard.local_status == Local.LOCAL_NOT_SUPPORTED
    assert token_guard.token_status == Token.TOKEN_NOT_VALID
    assert token_guard.quota_status == Quota.QUOTA_NOT_EVAL
    assert token_guard.blocked()


# TODO: Add baggage and context tests.


# =========================
# === Report Only Tests ===
# =========================


@pytest.mark.asyncio
async def test_guard_quota_report_only(report_only_guard, quota_service):
    """Check that quota is allowed when report only is enabled."""

    quota_service.GetTokenLease.return_value = quota_pb2.GetTokenLeaseResponse(
        granted=False,
        leases=[],
    )

    await report_only_guard.run()

    quota_service.GetTokenLease.assert_called_once()
    assert report_only_guard.local_status == Local.LOCAL_NOT_SUPPORTED
    assert report_only_guard.token_status == Token.TOKEN_EVAL_DISABLED
    assert report_only_guard.quota_status == Quota.QUOTA_BLOCKED
    assert report_only_guard.allowed()
