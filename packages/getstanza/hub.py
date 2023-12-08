import asyncio
import datetime
import logging
import os
from typing import Optional

import grpc
from getstanza.configuration import StanzaConfiguration
from getstanza.configuration_manager import StanzaConfigurationManager
from stanza.hub.v1 import auth_pb2_grpc, config_pb2_grpc, quota_pb2_grpc


class StanzaHub:
    """Implements all SDK to Stanza Hub interactions."""

    def __init__(self, config: StanzaConfiguration) -> None:
        # TODO: Send user-agent per SDK spec
        if os.environ.get("STANZA_HUB_NO_TLS"):  # disable TLS for local Hub development
            self.__grpc_channel = grpc.insecure_channel(config.hub_address)
        else:
            self.__grpc_channel = grpc.secure_channel(
                config.hub_address, grpc.ssl_channel_credentials()
            )

        # create Stanza Hub service stubs
        self.auth_service = auth_pb2_grpc.AuthServiceStub(self.__grpc_channel)
        self.config_service = config_pb2_grpc.ConfigServiceStub(self.__grpc_channel)
        self.quota_service = quota_pb2_grpc.QuotaServiceStub(self.__grpc_channel)

        # create initial configuration and poller
        self.config_manager = StanzaConfigurationManager(
            self.auth_service, self.config_service, config
        )
        self.hub_poller = StanzaHubPoller(
            config_manager=self.config_manager, interval=config.interval
        )

    def start_poller(self):
        """Start async polling of Hub for Service and Guard configs"""
        self.hub_poller.start()


class StanzaHubPoller:
    """Implements polling behavior for re-fetching configuration from Hub."""

    def __init__(
        self,
        config_manager: StanzaConfigurationManager,
        interval: datetime.timedelta,
    ):
        self.__polling_task: Optional[asyncio.Task[None]] = None
        self.__polling = False
        self.config_manager = config_manager
        self.interval = interval

    def start(self):
        """Begin polling with the configured interval."""

        self.__polling = True
        self.__schedule_poll()

    def stop(self):
        """Stop polling Hub for configuration changes."""

        if self.__polling_task:
            self.__polling_task.cancel()
            self.__polling = False

    async def __poll(self):
        """Polls for updated configuration information from Hub."""

        tasks = [
            asyncio.create_task(self.config_manager.fetch_service_config()),
            asyncio.create_task(self.config_manager.refetch_known_guard_configs()),
        ]
        await asyncio.wait(tasks)

    async def __poll_interval(self, _task: Optional[asyncio.Task[None]] = None):
        """Poll Hub then schedule another poll in the future using interval."""

        try:
            if self.__polling:
                await self.__poll()
        finally:
            if self.__polling:
                loop = asyncio.get_running_loop()
                loop.call_later(self.interval.total_seconds(), self.__schedule_poll)

    def __schedule_poll(self, _task: Optional[asyncio.Task[None]] = None):
        loop = asyncio.get_running_loop()
        self.__polling_task = loop.create_task(self.__poll_interval())
        self.__polling_task.add_done_callback(self.__handle_hub_poll_result)

    def __handle_hub_poll_result(self, task: asyncio.Task):
        try:
            task.result()
        except asyncio.CancelledError:
            pass  # Do not log task cancellations.
        except Exception as exc:
            logging.exception(
                "Received unexpected exception while polling Hub: %s", exc
            )
