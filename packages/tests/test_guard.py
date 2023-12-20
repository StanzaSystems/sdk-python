import pytest
from stanza.hub.v1 import quota_pb2
from stanza.hub.v1.common_pb2 import Local, Quota, Token


def test_guard_allows_default(guard):
    """Check that an unevaluated guard does not block by default."""

    assert guard.allowed()


@pytest.mark.asyncio
async def test_guard_quota_allowed(guard, quota_service):
    """Check that quota allowing works in a simple use case."""

    quota_service.GetTokenLease.return_value = quota_pb2.GetTokenLeaseResponse(
        granted=True,
        leases=[
            quota_pb2.TokenLease(
                duration_msec=86400,
                token="00000000",
                feature=None,
                priority_boost=1,
                weight=None,
                reason=None,
                expires_at=None,
                mode=None,
            )
        ],
    )

    await guard.run()

    assert guard.local_status == Local.LOCAL_NOT_SUPPORTED
    assert guard.token_status == Token.TOKEN_EVAL_DISABLED
    assert guard.quota_status == Quota.QUOTA_GRANTED
    assert guard.allowed()


@pytest.mark.asyncio
async def test_guard_quota_blocked(guard, quota_service):
    """Check that quota blocking works in a simple use case."""

    quota_service.GetTokenLease.return_value = quota_pb2.GetTokenLeaseResponse(
        granted=False,
        leases=[],
    )

    await guard.run()

    assert guard.local_status == Local.LOCAL_NOT_SUPPORTED
    assert guard.token_status == Token.TOKEN_EVAL_DISABLED
    assert guard.quota_status == Quota.QUOTA_BLOCKED
    assert guard.blocked()


@pytest.mark.asyncio
async def test_guard_quota_report_only(report_only_guard, quota_service):
    """Check that quota is allowed when report only is enabled."""

    quota_service.GetTokenLease.return_value = quota_pb2.GetTokenLeaseResponse(
        granted=False,
        leases=[],
    )

    await report_only_guard.run()

    assert report_only_guard.local_status == Local.LOCAL_NOT_SUPPORTED
    assert report_only_guard.token_status == Token.TOKEN_EVAL_DISABLED
    assert report_only_guard.quota_status == Quota.QUOTA_BLOCKED
    assert report_only_guard.allowed()
