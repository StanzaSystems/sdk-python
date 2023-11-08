import asyncio
import datetime
from typing import Optional

from getstanza.configuration_manager import StanzaConfigurationManager


class StanzaHubPoller:
    """Implements polling behavior for re-fetching configuration from Hub."""

    def __init__(
        self,
        configuration_manager: StanzaConfigurationManager,
        interval: datetime.timedelta,
    ):
        self.polling_task: Optional[asyncio.Task[None]] = None
        self.configuration_manager = configuration_manager
        self.interval = interval

    def begin(self):
        """Begin polling with the configured interval."""

        self.__schedule_poll()

    def __schedule_poll(self, _task: Optional[asyncio.Task[None]] = None):
        """Execute a poll against Hub and schedules another poll for later."""

        loop = asyncio.get_running_loop()
        self.polling_task = loop.create_task(self.__poll_hub())
        self.polling_task.add_done_callback(self.__schedule_poll)

    async def __poll_hub(self):
        """Polls for updated configuration information from hub."""

        # TODO: Await here once we get an asyncio compatible API client. Also
        # handle all guards that are in-use, not just service config.
        try:
            self.configuration_manager.fetch_service_config()
        finally:
            await asyncio.sleep(self.interval.total_seconds())
