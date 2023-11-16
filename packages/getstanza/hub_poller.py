import asyncio
import datetime
import logging
from typing import Optional

from getstanza.configuration_manager import StanzaConfigurationManager


class StanzaHubPoller:
    """Implements polling behavior for re-fetching configuration from Hub."""

    def __init__(
        self,
        configuration_manager: StanzaConfigurationManager,
        interval: datetime.timedelta,
    ):
        self.__polling_task: Optional[asyncio.Task[None]] = None
        self.__polling = False

        self.configuration_manager = configuration_manager
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

        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.configuration_manager.fetch_service_config())
            tg.create_task(self.configuration_manager.refetch_known_guard_configs())

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
