import asyncio
import datetime
import logging
from typing import Optional

from getstanza.hub.configuration_manager import StanzaHubConfigurationManager


class StanzaHubPoller:
    """Implements polling behavior for re-fetching configuration from Hub."""

    def __init__(
        self,
        event_loop: asyncio.AbstractEventLoop,
        config_manager: StanzaHubConfigurationManager,
        interval: datetime.timedelta,
    ):
        self.event_loop = event_loop
        self.config_manager = config_manager
        self.interval = interval

        self.__polling_task: Optional[asyncio.Task[None]] = None
        self.__polling = False

    def start(self):
        """Begin polling with the configured interval."""

        if not self.__polling:
            self.__polling = True
            self.event_loop.call_soon(self.__schedule_poll)

    def stop(self):
        """Stop polling Hub for configuration changes."""

        if self.__polling_task:
            self.__polling_task.cancel()
            self.__polling = False

    async def __poll(self):
        """Polls for updated configuration information from Hub."""

        configuration_fetch_tasks = [
            asyncio.create_task(self.config_manager.fetch_service_config()),
            asyncio.create_task(self.config_manager.refetch_known_guard_configs()),
        ]
        await asyncio.wait(configuration_fetch_tasks)

    async def __poll_interval(self, _task: Optional[asyncio.Task[None]] = None):
        """Poll Hub then schedule another poll in the future using interval."""

        try:
            if self.__polling:
                await self.__poll()
        finally:
            if self.__polling:
                self.event_loop.call_later(
                    self.interval.total_seconds(), self.__schedule_poll
                )

    def __schedule_poll(self):
        self.__polling_task = asyncio.create_task(self.__poll_interval())
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
