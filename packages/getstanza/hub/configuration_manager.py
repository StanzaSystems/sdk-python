import asyncio
import logging
from typing import MutableMapping, Optional, Tuple, TypedDict

import grpc
from getstanza.configuration import StanzaConfiguration
from stanza.hub.v1 import auth_pb2_grpc, common_pb2, config_pb2, config_pb2_grpc

VersionedGuardConfig = TypedDict(
    "VersionedGuardConfig",
    {
        "version": str,
        "config": config_pb2.GuardConfig,
    },
)


class StanzaHubConfigurationManager:
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

    async def get_guard_config(
        self, guard_name: str
    ) -> (Optional[config_pb2.GuardConfig], common_pb2.Config):
        """Retrieves the guard config for a specified guard."""

        if guard_name in self.__guard_configs:
            return (
                self.__guard_configs[guard_name]["config"],
                common_pb2.Config.CONFIG_CACHED_OK,
            )

        return await self.fetch_guard_config(guard_name)

    async def fetch_otel_bearer_token(self):
        """Fetch a new bearer token for use with the OTel collector."""
        try:
            bearer_token_response = self.__auth_service.GetBearerToken(
                metadata=self.config.metadata
            )
            self.__otel_bearer_token = bearer_token_response.bearer_token
        except grpc.RpcError as rpc_error:
            logging.debug(rpc_error.debug_error_string())  # type: ignore
            return

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
        except grpc.RpcError as rpc_error:
            logging.debug(rpc_error.debug_error_string())  # type: ignore
            return

        if service_config_response.config_data_sent:
            self.__service_config = service_config_response.config
            self.__service_config_version = service_config_response.version
            logging.debug(
                "Service config has changed from version '%s' to '%s'",
                last_version_seen,
                service_config_response.version,
            )

    async def fetch_guard_config(
        self, guard_name: str
    ) -> (Optional[config_pb2.GuardConfig], common_pb2.Config):
        """Fetch guard configuration changes for a specific guard."""

        existing_guard_config = self.__guard_configs.get(guard_name)
        last_version_seen = None
        if existing_guard_config:
            last_version_seen = existing_guard_config["version"]

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
        except grpc.RpcError as rpc_error:
            logging.debug(rpc_error.debug_error_string())  # type: ignore
            return None, common_pb2.Config.CONFIG_FETCH_ERROR

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
            return (
                self.__guard_configs[guard_name]["config"],
                common_pb2.Config.CONFIG_FETCHED_OK,
            )
        else:
            return None, common_pb2.Config.CONFIG_FETCHED_OK

    async def refetch_known_guard_configs(self):
        """Refetch all known instantiated guards."""

        tasks = []
        for guard_name in self.__guard_configs:
            tasks.append(asyncio.create_task(self.fetch_guard_config(guard_name)))
        if len(tasks) > 0:
            await asyncio.wait(tasks)
