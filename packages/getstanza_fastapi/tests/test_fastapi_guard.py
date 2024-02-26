import pytest
from fastapi import HTTPException, Request, status
from getstanza.client import StanzaClient
from getstanza.guard import GuardedStatus
from getstanza_fastapi.fastapi_guard import StanzaGuard


@pytest.fixture(autouse=True)
def context_from_http_headers(monkeypatch):
    def mock_context_from_http_headers():
        return None

    monkeypatch.setattr(StanzaClient, "getInstance", mock_context_from_http_headers)


class FakeGuard:
    def __init__(self, error=None, block_message=None, block_reason=None):
        self.success = GuardedStatus.GUARDED_SUCCESS
        self.failure = GuardedStatus.GUARDED_FAILURE
        self.error = error
        self.block_message = block_message
        self.block_reason = block_reason

    def blocked(self) -> bool:
        return self.block_message is not None

    def end(*args):
        pass


class FakeClient:
    def __init__(self, guard):
        self.__guard = guard

    async def guard(
        self,
        guard_name,
        feature=None,
        priority_boost=None,
        default_weight=None,
        tags=None,
    ):
        return self.__guard


@pytest.fixture()
def stanza_client_patcher(monkeypatch):
    def patcher(fake_guard: FakeGuard) -> None:
        def mock_getInstance():
            return FakeClient(fake_guard)

        monkeypatch.setattr(StanzaClient, "getInstance", mock_getInstance)

    return patcher


@pytest.fixture
def mock_request():
    return Request(scope={"type": "http", "headers": []})


def test_sync_guard_success(stanza_client_patcher, mock_request):
    stanza_client_patcher(FakeGuard())
    try:
        with StanzaGuard(mock_request, "MockGuard"):
            assert True
    except Exception:
        assert False


def test_sync_guard_blocked(mock_request, stanza_client_patcher):
    stanza_client_patcher(
        FakeGuard(block_message="fake block", block_reason="fake reason")
    )
    try:
        with StanzaGuard(mock_request, "MockGuard"):
            assert False
    except HTTPException as req_exc:
        assert req_exc.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        assert req_exc.detail == {
            "message": "fake block",
            "reason": "fake reason",
        }


def test_sync_guard_error(caplog, mock_request, stanza_client_patcher):
    stanza_client_patcher(FakeGuard(error="fake error"))
    try:
        with StanzaGuard(mock_request, "MockGuard"):
            assert True
    except Exception:
        assert False
    finally:
        assert "fake error" in caplog.text


@pytest.mark.asyncio
async def test_async_guard(mock_request, stanza_client_patcher):
    stanza_client_patcher(FakeGuard())
    try:
        async with StanzaGuard(mock_request, "MockGuard"):
            assert True
    except Exception:
        assert False
