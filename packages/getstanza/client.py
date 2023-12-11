import logging
from typing import Optional

from getstanza.configuration import StanzaConfiguration
from getstanza.guard import Guard
from getstanza.hub import StanzaHub


class StanzaClient:
    """
    SDK client that assists with integrating with Hub and managing the active
    service and guard configurations.
    """

    def __init__(self, config: StanzaConfiguration):
        logging.debug("Initializing Stanza")

        self.config = config
        self.__hub = StanzaHub(config)

        # TODO: Add refetch logic for this whenever 'exp' happens.
        # self.__hub.fetch_otel_bearer_token()

        # TODO: Initialize OTEL TextMapPropagator here
        # otel.InitTextMapPropagator(otel.StanzaHeaders{})

        # TODO: Consider allowing this all to be setup on another thread so this
        # works well with synchronous frameworks like Flask?

        # TODO: Pass configuration and dependencies around using a context?

        self.__hub.start_poller()

    async def guard(
        self,
        guard_name: str,
        feature: Optional[str] = None,
        priority_boost: Optional[int] = None,
        tags=None,
    ) -> Guard:
        """Initialize a guard and fetch its configuration if not cached."""

        (
            guard_config,
            guard_config_status,
        ) = await self.__hub.config_manager.get_guard_config(guard_name)

        guard = Guard(
            self.__hub.quota_service,
            self.config,
            guard_config,
            guard_config_status,
            guard_name,
            feature_name=feature,
            priority_boost=priority_boost,
            tags=tags,
        )
        await guard.run()

        return guard
