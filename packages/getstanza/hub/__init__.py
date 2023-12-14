import os

import grpc
from getstanza.configuration import StanzaConfiguration
from getstanza.hub.configuration_manager import StanzaHubConfigurationManager
from getstanza.hub.poller import StanzaHubPoller
from stanza.hub.v1 import auth_pb2_grpc, config_pb2_grpc, quota_pb2_grpc


class StanzaHub:
    """Implements all SDK to Stanza Hub interactions."""

    def __init__(self, config: StanzaConfiguration) -> None:
        # TODO: Send user-agent per SDK spec
        if os.environ.get("STANZA_HUB_NO_TLS"):  # Disable TLS for local Hub development
            self.__grpc_channel = grpc.insecure_channel(config.hub_address)
        else:
            self.__grpc_channel = grpc.secure_channel(
                config.hub_address, grpc.ssl_channel_credentials()
            )

        # Create Stanza Hub service stubs.
        self.auth_service = auth_pb2_grpc.AuthServiceStub(self.__grpc_channel)
        self.config_service = config_pb2_grpc.ConfigServiceStub(self.__grpc_channel)
        self.quota_service = quota_pb2_grpc.QuotaServiceStub(self.__grpc_channel)

        # Create initial configuration and poller.
        self.config_manager = StanzaHubConfigurationManager(
            self.auth_service,
            self.config_service,
            config,
        )
        self.hub_poller = StanzaHubPoller(
            config_manager=self.config_manager,
            interval=config.interval,
        )

    def start_poller(self):
        """Start async polling of Hub for Service and Guard configs"""

        self.hub_poller.start()
