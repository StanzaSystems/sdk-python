from unittest.mock import patch

import pytest


@pytest.fixture
def quota_service():
    with patch("stanza.hub.v1.quota_pb2_grpc.QuotaServiceStub") as MockClass:
        instance = MockClass.return_value
        instance.GetToken.return_value = None
        instance.GetTokenLease.return_value = None
        instance.SetTokenLeaseConsumed.return_value = None
        instance.ValidateToken.return_value = None

        yield instance
