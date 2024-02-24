from unittest.mock import patch

import pytest
from fastapi import HTTPException, Request, status
from getstanza.guard import Guard
from getstanza_fastapi.fastapi_guard import StanzaGuard


@pytest.fixture(autouse=True)
def context_from_http_headers():
    with patch("getstanza.propagation.context_from_http_headers") as MockClass:
        MockClass.return_value = None


class FakeGuard(Guard):
    def __init__(self):
        self.__is_blocked = False

    def set_error(self, error: str):
        self.__error_message = error

    def set_is_blocked(self, blocked: bool):
        self.__is_blocked = blocked

    def blocked(self) -> bool:
        return self.__is_blocked

    @property
    def block_message(self):
        return "fake block"

    @property
    def block_reason(self):
        return "fake reason"


@pytest.fixture()
def stanza_client_patcher():
    def patch_guard() -> FakeGuard:
        fake_guard = FakeGuard()
        with patch("getstanza.client.StanzaClient.getInstance") as MockClass:
            MockClass.return_value = fake_guard
        return fake_guard

    return patch_guard


@pytest.fixture
def mock_request():
    return Request(scope={"type": "http", "headers": []})


def test_sync_guard_success(mock_request, stanza_client_patcher):
    stanza_client_patcher()
    with StanzaGuard(mock_request, "MockGuard"):
        try:
            assert True
        except Exception:
            assert False


def test_sync_guard_blocked(mock_request, stanza_client_patcher):
    fake_guard = stanza_client_patcher()
    fake_guard.set_is_blocked(True)
    with StanzaGuard(mock_request, "MockGuard"):
        try:
            assert False
        except HTTPException as req_exc:
            assert req_exc.status_code == status.HTTP_429_TOO_MANY_REQUESTS
            assert req_exc.detail == {
                "message": "fake block",
                "reason": "fake reason",
            }


def test_sync_guard_error(mock_request, stanza_client_patcher):
    with StanzaGuard(mock_request, "MockGuard"):
        try:
            assert True
        finally:
            # TODO: patch logging.error to save to a variable so we can assert it logged the correct error
            pass


@pytest.mark.asyncio
async def test_async_guard(mock_request, stanza_client_patcher):
    """Tests that the async versions of entry execute and end the guard correctly"""

    stanza_client_patcher()
    async with StanzaGuard(mock_request, "MockGuard"):
        try:
            assert True
        except Exception:
            assert False
