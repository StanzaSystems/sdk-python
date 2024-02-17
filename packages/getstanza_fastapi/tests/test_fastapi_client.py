from unittest.mock import patch

import pytest
from fastapi import Request
from getstanza.configuration import StanzaConfiguration
from getstanza.tests.utils import async_return
from getstanza_fastapi.fastapi_client import StanzaFastAPIClient

# TODO: Test the context manager by itself as well.


@pytest.fixture
def fastapi_guard():
    with patch("getstanza_fastapi.fastapi_guard.StanzaGuard") as MockClass:
        instance = MockClass.return_value
        instance.__aenter__.return_value = async_return(None)
        instance.__aexit__.return_value = async_return(None)
        instance.__enter__.return_value = None
        instance.__exit__.return_value = None

        yield instance


@pytest.fixture
def fastapi_client(fastapi_guard):
    return StanzaFastAPIClient(
        StanzaConfiguration(
            api_key="MOCK_API_KEY",
            service_name="fastapi-mock",
            service_release="0.0.1",
            environment="dev",
            hub_address="hub.fake.getstanza.dev:9020",
        )
    )


@pytest.fixture
def mock_request():
    return Request(scope={"type": "http", "headers": []})


@pytest.mark.asyncio
async def test_async_wrapper(fastapi_client, fastapi_guard, mock_request):
    @fastapi_client.stanza_guard("MockGuard")
    async def mock_handler(request: Request):
        return {"mock": "response"}

    await mock_handler(mock_request)

    fastapi_guard.__aenter__.assert_called_once()
    fastapi_guard.__aexit__.assert_called_once()
