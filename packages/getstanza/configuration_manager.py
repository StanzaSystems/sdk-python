import asyncio
import json
import logging
from typing import MutableMapping, Optional, TypedDict

from getstanza import hub
from getstanza.configuration import StanzaConfiguration
from getstanza.errors.hub import hub_error
from getstanza.hub.api.config_service_api import ConfigServiceApi
from getstanza.hub.api_client import ApiClient
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

    def __init__(self, api_client: ApiClient, config: StanzaConfiguration):
        self.api_client = api_client
        self.config = config

        self.__config_service = ConfigServiceApi(self.api_client)

        # TODO: Utilize type aliases whenever we upgrade to Python 3.12.
        self.__service_config: Optional[V1ServiceConfig] = None
        self.__service_config_version: Optional[str] = None
        self.__guard_configs: MutableMapping[str, VersionedGuardConfig] = {}

    def get_guard_config(self, guard_name: str) -> Optional[hub.V1GuardConfig]:
        """Retrieves the guard config for a specified guard."""

        return (
            self.__guard_configs[guard_name]["config"]
            if guard_name in self.__guard_configs
            else None
        )

    async def fetch_service_config(self):
        """Fetch service configuration changes."""

        try:
            service_config_response = (
                await self.__config_service.config_service_get_service_config(
                    async_req=True,
                    body=V1GetServiceConfigRequest(
                        version_seen=self.__service_config_version,
                        service=V1ServiceSelector(
                            environment=self.config.environment,
                            name=self.config.service_name,
                            release=self.config.service_release,
                        ),
                        client_id=self.config.client_id,
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

    async def fetch_guard_config(self, guard_name: str) -> V1GuardConfig:
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
                            environment=self.config.environment,
                            guard_name=guard_name,
                            service_name=self.config.service_name,
                            service_release=self.config.service_release,
                        ),
                    ),
                ).get()
            )
        except ApiException as exc:
            raise hub_error(exc) from exc

        if guard_config_response.config_data_sent:
            guard_config = {
                "version": guard_config_response.version,
                "config": guard_config_response.config,
            }
            self.__guard_configs[guard_name] = guard_config

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

            return guard_config["config"]

        return self.__guard_configs[guard_name]["config"]

    async def refetch_known_guard_configs(self):
        """Refetch all known instantiated guards."""

        async with asyncio.TaskGroup() as tg:
            for guard_name in self.__guard_configs:
                tg.create_task(self.fetch_guard_config(guard_name))
