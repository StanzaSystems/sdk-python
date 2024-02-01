import asyncio
import logging
import random
from typing import Optional

from getstanza.hub.configuration_manager import StanzaHubConfigurationManager

# Set to less than the maximum duration of the Auth0 Bearer Token
BEARER_TOKEN_REFRESH_INTERVAL_SECS = 43_000
BEARER_TOKEN_REFRESH_JITTER_SECS = 200


class StanzaTelemetryCollector:
    """Implements reconnecting to Stanza's OpenTelemetry collector."""

    def __init__(
        self,
        event_loop: asyncio.AbstractEventLoop,
        config_manager: StanzaHubConfigurationManager,
    ):
        self.event_loop = event_loop
        self.config_manager = config_manager

        self.__task: Optional[asyncio.Task[None]] = None
        self.event_loop.call_later(self.__jitter(), self.__schedule)

    def __jitter(self) -> float:
        return BEARER_TOKEN_REFRESH_INTERVAL_SECS + random.randint(
            0, BEARER_TOKEN_REFRESH_JITTER_SECS
        )

    async def __connect(self):
        await asyncio.wait([asyncio.create_task(self.config_manager.connect_otel())])

    async def __interval(self):
        try:
            await self.__connect()
        finally:
            self.event_loop.call_later(self.__jitter(), self.__schedule)

    def __schedule(self):
        self.__task = asyncio.create_task(self.__interval())
        self.__task.add_done_callback(self.__handle_result)

    def __handle_result(self, task: asyncio.Task):
        try:
            task.result()
        except asyncio.CancelledError:
            pass  # Do not log task cancellations.
        except Exception as exc:
            logging.exception(
                "Received unexpected exception while connecting to OTEL collector: %s",
                exc,
            )
