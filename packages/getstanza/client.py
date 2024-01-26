import logging
import threading
from typing import Optional, cast

from getstanza.configuration import StanzaConfiguration
from getstanza.guard import Guard
from getstanza.hub import StanzaHub
from typing_extensions import Self


class StanzaClient:
    """
    SDK client that assists with integrating with Hub and managing the active
    service and guard configurations.
    """

    __instance: Optional[Self] = None
    __lock = threading.Lock()

    @property
    def config(self) -> StanzaConfiguration:
        return self.__config

    @property
    def hub(self) -> Optional[StanzaHub]:
        return self.__hub

    @classmethod
    def getInstance(cls) -> Self:
        """Returns the global instance of the Stanza SDK client."""

        if cls.__instance is None:
            raise RuntimeError("The Stanza SDK has not yet been initialized")

        return cast(Self, cls.__instance)

    def __init__(self, config: StanzaConfiguration):
        """Initializes the Stanza SDK. This can only happen once."""

        logging.debug("Initializing Stanza")

        self.__config = config
        self.__hub = None

        if StanzaClient.__instance is None:
            with StanzaClient.__lock:
                if StanzaClient.__instance is None:
                    StanzaClient.__instance = self
                    self.__start_poller()
                    return

        raise RuntimeError("The Stanza SDK client has already been initialized")

    def __start_poller(self):
        """Initialize the Hub worker and start it on a new thread."""

        def target():
            self.__hub = StanzaHub(self.__config)
            self.__hub.start_poller()

        # We don't worry about cleaning this up since the SDK client instance
        # persists for the lifetime of the process, and only one can exist.
        # Being marked as a daemon thread, this thread will not stop signals
        # from killing the process.
        threading.Thread(target=target, daemon=True).start()

    async def guard(
        self,
        guard_name: str,
        feature: Optional[str] = None,
        priority_boost: Optional[int] = None,
        default_weight: Optional[float] = None,
        tags=None,
    ) -> Guard:
        """Initialize a guard and fetch its configuration if not cached."""

        if self.__hub is None:
            raise RuntimeError("The Stanza SDK client hasn't been initialized yet")

        guard = Guard(
            self.__hub,
            guard_name,
            feature_name=feature,
            priority_boost=priority_boost,
            default_weight=default_weight,
            tags=tags,
        )
        await guard.run()

        return guard
