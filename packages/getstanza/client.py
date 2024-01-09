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
    def config(self):
        return self.__config

    @property
    def hub(self):
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

        if StanzaClient.__instance is None:
            with StanzaClient.__lock:
                if StanzaClient.__instance is None:
                    self.__config = config
                    self.__hub = StanzaHub(config)
                    StanzaClient.__instance = self
                    self.__hub.start_poller()
                    return

        raise RuntimeError("The Stanza SDK client has already been initialized")

    async def guard(
        self,
        guard_name: str,
        feature: Optional[str] = None,
        priority_boost: Optional[int] = None,
        default_weight: Optional[float] = None,
        tags=None,
    ) -> Guard:
        """Initialize a guard and fetch its configuration if not cached."""

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
