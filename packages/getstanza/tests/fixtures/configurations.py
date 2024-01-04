import pytest
from getstanza.configuration import StanzaConfiguration

TEST_API_KEY = "0000000000000000000000000000000000000000000000000000000000000000"
TEST_SERVICE_NAME = "TestService"
TEST_SERVICE_RELEASE = "0.0.0"
TEST_ENVIRONMENT = "dev"
TEST_HUB_ADDRESS = "127.0.0.1:9060"


@pytest.fixture
def stanza_config():
    return StanzaConfiguration(
        api_key=TEST_API_KEY,
        service_name=TEST_SERVICE_NAME,
        service_release=TEST_SERVICE_RELEASE,
        environment=TEST_ENVIRONMENT,
        hub_address=TEST_HUB_ADDRESS,
    )
