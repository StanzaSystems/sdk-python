from unittest.mock import patch

import pytest


@pytest.fixture
def stanza_hub(config_manager, quota_service):
    with patch("getstanza.hub.StanzaHub") as MockClass:
        instance = MockClass.return_value
        instance.quota_service = quota_service
        instance.config_manager = config_manager

        yield instance


@pytest.fixture
def config_manager(stanza_config):
    with patch("getstanza.hub.StanzaHubConfigurationManager") as MockClass:
        instance = MockClass.return_value
        instance.config = stanza_config
        instance.get_guard_config.return_value = None

        yield instance


@pytest.fixture
def quota_service():
    with patch("stanza.hub.v1.quota_pb2_grpc.QuotaServiceStub") as MockClass:
        instance = MockClass.return_value
        instance.GetToken.return_value = None
        instance.GetTokenLease.return_value = None
        instance.SetTokenLeaseConsumed.return_value = None
        instance.ValidateToken.return_value = None

        yield instance
