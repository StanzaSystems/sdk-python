import asyncio
import os

import grpc
from getstanza.configuration import StanzaConfiguration
from getstanza.hub.configuration_manager import StanzaHubConfigurationManager
from getstanza.hub.poller import StanzaHubPoller
from getstanza.hub.telemetry import StanzaTelemetryCollector
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

        try:
            asyncio.get_running_loop()
        except RuntimeError:
            pass  # Expected result as we want no event loop running yet.
        else:
            raise RuntimeError(
                "Cannot create an event loop for Hub as this thread already "
                "has a loop initialized."
            )

        # Other threads will need to interact with Stanza. We keep a reference
        # to the loop being used by the SDK client from the thread it was
        # initialized on to ensure that any new recurring tasks spawned from
        # other threads are able to run for the duration of the SDK client's
        # lifetime.
        self.event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.event_loop)

        # Create Stanza Hub service stubs.
        self.auth_service = auth_pb2_grpc.AuthServiceStub(self.__grpc_channel)
        self.config_service = config_pb2_grpc.ConfigServiceStub(self.__grpc_channel)
        self.quota_service = quota_pb2_grpc.QuotaServiceStub(self.__grpc_channel)

        # Create initial configuration and poller.
        self.config_manager = StanzaHubConfigurationManager(
            auth_service=self.auth_service,
            config_service=self.config_service,
            config=config,
        )
        self.hub_poller = StanzaHubPoller(
            event_loop=self.event_loop,
            config_manager=self.config_manager,
            interval=config.interval,
        )
        self.telemetry_collector = StanzaTelemetryCollector(
            event_loop=self.event_loop,
            config_manager=self.config_manager,
        )

    def start_poller(self):
        """Start async polling of Hub for Service and Guard configs"""

        self.hub_poller.start()
        self.event_loop.run_forever()
