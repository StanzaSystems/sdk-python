import pytest
from stanza.hub.v1 import quota_pb2
from stanza.hub.v1.common_pb2 import Local, Quota, Token


def test_guard_allows_default(quota_guard):
    """Check that an unevaluated guard does not block by default."""

    assert quota_guard.allowed()


@pytest.mark.asyncio
async def test_guard_allows_when_config_null(quota_service, guard_without_config):
    """It should allow if getting the configuration fails (config is null)"""

    await guard_without_config.run()

    quota_service.GetTokenLease.assert_not_called()
    assert guard_without_config.local_status == Local.LOCAL_NOT_EVAL
    assert guard_without_config.token_status == Token.TOKEN_NOT_EVAL
    assert guard_without_config.quota_status == Quota.QUOTA_NOT_EVAL
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
async def test_guard_blocks_when_config_not_found(quota_service, guard_without_config_not_found):
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

    quota_service.GetTokenLease.assert_called_once()
    assert quota_guard.local_status == Local.LOCAL_NOT_SUPPORTED
    assert quota_guard.token_status == Token.TOKEN_EVAL_DISABLED
    assert quota_guard.quota_status == Quota.QUOTA_GRANTED
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
    assert quota_guard.blocked()


# TODO: Clear global cached and consumed lease state between each test.


# === Guard Quota Tests ===
#
# It should request quota with specified feature
# It should request quota with specified priority boost
# It should request quota with sum of specified priority boost and value from baggage

# TODO: Add baggage and context tests.
#
# It should request quota with feature from baggage
# It should request quota with priority boost from baggage

# ===========================
# === Ingress Token Tests ===
# ===========================

# === Guard Ingress Token Tests ===
#
# It should NOT be pass-through execution after config is fetched.
# It should validate token before proceeding with execution
# It should fail the execution if token is not validated
# It should NOT be pass-through execution after config is fetched
# It should proceed execution if validating token throws
# It should proceed execution if validating token takes more than 1000ms
# It should fail the execution if ingress token is validated but new token is not granted

# TODO: Add baggage and context tests.
#
# It should error execution after config is fetched and no token is provided in context


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


# === SDK Client Level Guard Tests ===
#
# It should fetch guard config upon initialization.
# It should allow if getting the configuration fails.
# It should block execution until the service configuration is fetched.

# === Configuration Manager Level Tests ===
#
# It should only fetch guard configurations once when invoked multiple times.
# It should fetch guard config only once upon initialization of the same guard
#    multiple times - with different features and priority boosts.
# It should fetch guard config only once per different.
