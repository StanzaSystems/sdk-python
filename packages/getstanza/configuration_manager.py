import asyncio
import json
import logging
import uuid
from typing import MutableMapping, Optional, TypedDict

from getstanza import hub
from getstanza.configuration import StanzaConfiguration
from getstanza.errors.hub import hub_error
from getstanza.hub.api.auth_service_api import AuthServiceApi
from getstanza.hub.api.config_service_api import ConfigServiceApi
from getstanza.hub.api_client import ApiClient
from getstanza.hub.configuration import Configuration
from getstanza.hub.models.v1_get_guard_config_request import V1GetGuardConfigRequest
from getstanza.hub.models.v1_get_service_config_request import V1GetServiceConfigRequest
from getstanza.hub.models.v1_guard_config import V1GuardConfig
from getstanza.hub.models.v1_guard_service_selector import V1GuardServiceSelector
from getstanza.hub.models.v1_service_config import V1ServiceConfig
from getstanza.hub.models.v1_service_selector import V1ServiceSelector
from getstanza.hub.rest import ApiException

VersionedGuardConfig = TypedDict(
    "VersionedGuardConfig",
    {
        "version": str,
        "config": V1GuardConfig,
    },
)


class StanzaConfigurationManager:
    """State manager for the active service configuration."""

    def __init__(self, config: StanzaConfiguration):
        self.api_key = config.api_key
        self.service_name = config.service_name
        self.release = config.service_release
        self.environment = config.environment
        self.hub_address = config.hub_address
        self.client_id = str(uuid.uuid4())

        configuration = Configuration()
        configuration.host = config.hub_address
        configuration.api_key["X-Stanza-Key"] = config.api_key
        api_client = ApiClient(configuration)

        self.__config_service = ConfigServiceApi(api_client)
        self.__auth_service = AuthServiceApi(api_client)

        # TODO: Utilize type aliases whenever we upgrade to Python 3.12.
        self.__service_config: Optional[V1ServiceConfig] = None
        self.__service_config_version: Optional[str] = None
        self.__guard_configs: MutableMapping[str, VersionedGuardConfig] = {}
        self.__bearer_token: Optional[str] = None

        # TODO: Add refetch logic for this whenever 'exp' happens.
        # self.fetch_otel_bearer_token()

    def get_guard_config(self, guard_name: str) -> Optional[hub.V1GuardConfig]:
        """Retrieves the guard config for a specified guard."""

        return (
            self.__guard_configs[guard_name]["config"]
            if guard_name in self.__guard_configs
            else None
        )

    async def fetch_otel_bearer_token(self):
        """Fetch a new bearer token for use with the OTel collector."""

        try:
            bearer_token_response = (
                await self.__auth_service.auth_service_get_bearer_token(
                    async_req=True,
                    environment=self.environment,
                ).get()
            )
            self.__bearer_token = bearer_token_response.bearer_token
        except ApiException as exc:
            raise hub_error(exc) from exc

    async def fetch_service_config(self):
        """Fetch service configuration changes."""

        try:
            service_config_response = (
                await self.__config_service.config_service_get_service_config(
                    async_req=True,
                    body=V1GetServiceConfigRequest(
                        version_seen=self.__service_config_version,
                        service=V1ServiceSelector(
                            environment=self.environment,
                            name=self.service_name,
                            release=self.release,
                        ),
                        client_id=self.client_id,
                    ),
                ).get()
            )
        except ApiException as exc:
            raise hub_error(exc) from exc

        if service_config_response.config_data_sent:
            self.__service_config = service_config_response.config
            self.__service_config_version = service_config_response.version

            logging.debug(
                "Service config has changed from version '%s' to '%s'",
                service_config_response.version,
                self.__service_config_version,
            )
            logging.debug(
                "New active service config: %s",
                json.dumps(self.__service_config.to_dict(), indent=2, sort_keys=True),
            )

    async def fetch_guard_config(self, guard_name: str):
        """Refetch guard configuration changes for a specific guard."""

        existing_guard_config = self.__guard_configs.get(guard_name)
        last_version_seen = existing_guard_config and existing_guard_config["version"]

        try:
            guard_config_response = (
                await self.__config_service.config_service_get_guard_config(
                    async_req=True,
                    body=V1GetGuardConfigRequest(
                        version_seen=last_version_seen,
                        selector=V1GuardServiceSelector(
                            environment=self.environment,
                            guard_name=guard_name,
                            service_name=self.service_name,
                            service_release=self.release,
                        ),
                    ),
                ).get()
            )
        except ApiException as exc:
            raise hub_error(exc) from exc

        if guard_config_response.config_data_sent:
            self.__guard_configs[guard_name] = {
                "version": guard_config_response.version,
                "config": guard_config_response.config,
            }

            logging.debug(
                "Guard config for guard '%s' has changed from version '%s' to '%s'",
                guard_name,
                last_version_seen,
                guard_config_response.version,
            )
            logging.debug(
                "New active guard config for guard '%s': %s",
                guard_name,
                json.dumps(
                    guard_config_response.config.to_dict(), indent=2, sort_keys=True
                ),
            )

    async def refetch_known_guard_configs(self):
        """Refetch all known instantiated guards."""

        async with asyncio.TaskGroup() as tg:
            for guard_name in self.__guard_configs:
                tg.create_task(self.fetch_guard_config(guard_name))
