from unittest.mock import patch

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
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


@pytest.fixture(scope="module")
def fastapi_client():
    return StanzaFastAPIClient(
        StanzaConfiguration(
            api_key="MOCK_API_KEY",
            service_name="fastapi-mock",
            service_release="0.0.1",
            environment="dev",
            hub_address="localhost",
        )
    )


@pytest.fixture(scope="module")
def fastapi_app():
    return FastAPI()


@pytest.fixture(scope="module")
def fastapi_testclient(fastapi_app):
    return TestClient(fastapi_app)


@pytest.mark.asyncio
async def test_async_wrapper_without_request(
    fastapi_client, fastapi_guard, fastapi_app, fastapi_testclient
):
    @fastapi_app.get("/")
    @fastapi_client.stanza_guard("MockGuard")
    async def mock_endpoint(request: Request):
        return {"mock": "response"}

    response = fastapi_testclient.get("/")
    assert response.status_code == 200
    assert response.json() == {"mock": "response"}

    fastapi_guard.__aenter__.assert_called_once()
    fastapi_guard.__aexit__.assert_called_once()


@pytest.mark.asyncio
async def test_async_wrapper_with_request(
    fastapi_client, fastapi_guard, fastapi_app, fastapi_testclient
):
    @fastapi_app.get("/")
    @fastapi_client.stanza_guard("MockGuard")
    async def mock_endpoint():
        return {"mock": "response"}

    response = fastapi_testclient.get("/")
    assert response.status_code == 200
    assert response.json() == {"mock": "response"}

    fastapi_guard.__aenter__.assert_called_once()
    fastapi_guard.__aexit__.assert_called_once()
