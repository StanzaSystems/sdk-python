import logging
from typing import Optional

from getstanza.configuration import StanzaConfiguration
from getstanza.configuration_manager import StanzaConfigurationManager
from getstanza.errors.hub import hub_error
from getstanza.guard import Guard
from getstanza.hub.api.auth_service_api import AuthServiceApi
from getstanza.hub.api_client import ApiClient
from getstanza.hub.configuration import Configuration
from getstanza.hub.rest import ApiException
from getstanza.hub_poller import StanzaHubPoller


class StanzaClient:
    """
    SDK client that assists with integrating with Hub and managing the active
    service and guard configurations.
    """

    def __init__(self, config: StanzaConfiguration):
        configuration = Configuration()
        configuration.host = config.hub_address
        configuration.api_key["X-Stanza-Key"] = config.api_key
        self.api_client = ApiClient(configuration)

        self.config = config
        self.config_manager = StanzaConfigurationManager(self.api_client, config)
        self.hub_poller = StanzaHubPoller(
            config_manager=self.config_manager, interval=config.interval
        )

        self.__auth_service = AuthServiceApi(self.api_client)
        self.__bearer_token: Optional[str] = None

        # TODO: Add refetch logic for this whenever 'exp' happens.
        # self.fetch_otel_bearer_token()

        # TODO: Initialize OTEL TextMapPropagator here
        # otel.InitTextMapPropagator(otel.StanzaHeaders{})

        # TODO: Consider allowing this all to be setup on another thread so this
        # works well with synchronous frameworks like Flask?

        # TODO: Pass configuration and dependencies around using a context?

    def init(self):
        """Use to initialize the Stanza SDK."""

        logging.debug("Initializing Stanza")

        self.hub_poller.start()

    async def fetch_otel_bearer_token(self):
        """Fetch a new bearer token for use with the OTel collector."""

        try:
            bearer_token_response = (
                await self.__auth_service.auth_service_get_bearer_token(
                    async_req=True,
                    environment=self.config.environment,
                ).get()
            )
            self.__bearer_token = bearer_token_response.bearer_token
        except ApiException as exc:
            raise hub_error(exc) from exc

    async def guard(
        self,
        guard_name: str,
        feature: Optional[str] = None,
        priority_boost: Optional[int] = None,
        tags=None,
    ) -> Guard:
        """Initialize a guard and fetch its configuration if not cached."""

        guard_config = self.config_manager.get_guard_config(guard_name)
        if not guard_config:
            guard_config = await self.config_manager.fetch_guard_config(guard_name)

        guard = Guard(
            self.api_client,
            self.config,
            guard_config,
            guard_name,
            feature_name=feature,
            priority_boost=priority_boost,
            tags=tags,
        )
        await guard.run()

        return guard
