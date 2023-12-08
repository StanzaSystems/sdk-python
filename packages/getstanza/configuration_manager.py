import asyncio

# import json
import logging
from typing import MutableMapping, Optional, TypedDict

from getstanza.configuration import StanzaConfiguration
from getstanza.errors.hub import hub_error

# import stanza.hub.v1 as hubv1
# from stanza.hub.v1 import config_pb2 as hubv1_config
# from stanza.hub.v1.config_pb2 import GetGuardConfigRequest
# import stanza.hub.v1.config_pb2 as stanza_dot_hub_dot_v1_dot_config__pb2
# from stanza.hub.v1 import config_pb2 as hubv1_config
from stanza.hub.v1 import auth_pb2_grpc, common_pb2, config_pb2, config_pb2_grpc

VersionedGuardConfig = TypedDict(
    "VersionedGuardConfig",
    {
        "version": str,
        "config": config_pb2.GuardConfig,
    },
)


class StanzaConfigurationManager:
    """State manager for the active service configuration."""

    def __init__(
        self,
        auth_service: auth_pb2_grpc.AuthServiceStub,
        config_service: config_pb2_grpc.ConfigServiceStub,
        config: StanzaConfiguration,
    ):
        self.config = config

        self.__auth_service = auth_service
        self.__config_service = config_service

        # TODO: Utilize type aliases whenever we upgrade to Python 3.12.
        self.__service_config: Optional[config_pb2.ServiceConfig] = None
        self.__service_config_version: Optional[str] = None
        self.__guard_configs: MutableMapping[str, VersionedGuardConfig] = {}

    def get_guard_config(self, guard_name: str) -> Optional[config_pb2.GuardConfig]:
        """Retrieves the guard config for a specified guard."""

        return (
            self.__guard_configs[guard_name]["config"]
            if guard_name in self.__guard_configs
            else None
        )

    async def fetch_otel_bearer_token(self):
        """Fetch a new bearer token for use with the OTel collector."""
        try:
            bearer_token_response = self.__auth_service.GetBearerToken(
                metadata=self.config.metadata
            )
            self.__otel_bearer_token = bearer_token_response.bearer_token
        except Exception as exc:
            raise hub_error(exc) from exc

    async def fetch_service_config(self):
        """Fetch service configuration changes."""

        last_version_seen = self.__service_config_version
        try:
            service_config_response = self.__config_service.GetServiceConfig(
                metadata=self.config.metadata,
                request=config_pb2.GetServiceConfigRequest(
                    client_id=self.config.client_id,
                    version_seen=last_version_seen,
                    service=common_pb2.ServiceSelector(
                        name=self.config.service_name,
                        release=self.config.service_release,
                        environment=self.config.environment,
                    ),
                ),
            )
        except Exception as exc:
            raise hub_error(exc) from exc

        if service_config_response.config_data_sent:
            self.__service_config = service_config_response.config
            self.__service_config_version = service_config_response.version
            logging.debug(
                "Service config has changed from version '%s' to '%s'",
                last_version_seen,
                service_config_response.version,
            )

    async def fetch_guard_config(self, guard_name: str) -> config_pb2.GuardConfig:
        """Fetch guard configuration changes for a specific guard."""

        existing_guard_config = self.__guard_configs.get(guard_name)
        last_version_seen = existing_guard_config and existing_guard_config["version"]

        try:
            guard_config_response = self.__config_service.GetGuardConfig(
                metadata=self.config.metadata,
                request=config_pb2.GetGuardConfigRequest(
                    version_seen=last_version_seen,
                    selector=common_pb2.GuardServiceSelector(
                        guard_name=guard_name,
                        service_name=self.config.service_name,
                        service_release=self.config.service_release,
                        environment=self.config.environment,
                    ),
                ),
            )
        except Exception as exc:
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

        return self.__guard_configs[guard_name]["config"]

    async def refetch_known_guard_configs(self):
        """Refetch all known instantiated guards."""

        tasks = [
            asyncio.create_task(
                self.fetch_guard_config(guard_name)
                for guard_name in self.__guard_configs
            )
        ]
        await asyncio.wait(tasks)
