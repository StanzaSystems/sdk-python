import asyncio
import logging
import os
import threading
from collections import defaultdict
from typing import MutableMapping, Optional, TypedDict, cast

import grpc
from getstanza.configuration import StanzaConfiguration
from getstanza.otel import OpenTelemetry
from stanza.hub.v1 import (
    auth_pb2,
    auth_pb2_grpc,
    common_pb2,
    config_pb2,
    config_pb2_grpc,
)

DEFAULT_TIMEOUT = 300

VersionedGuardConfig = TypedDict(
    "VersionedGuardConfig",
    {
        "version": str,
        "config": config_pb2.GuardConfig,
    },
)

service_config_lock = threading.Lock()
guard_config_locks = defaultdict(threading.Lock)


class StanzaHubConfigurationManager:
    """State manager for the active service configuration."""

    @property
    def service_config(self):
        return self.__service_config

    @property
    def otel(self):
        return self.__otel

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
        self.__otel: Optional[OpenTelemetry] = None

    async def get_guard_config(
        self, guard_name: str
    ) -> (tuple[config_pb2.GuardConfig, common_pb2.Config]):
        """Retrieves the guard config for a specified guard."""

        if guard_name in self.__guard_configs:
            return (
                self.__guard_configs[guard_name]["config"],
                common_pb2.Config.CONFIG_CACHED_OK,
            )

        return await self.fetch_guard_config(guard_name)

    async def fetch_otel_bearer_token(self) -> str:
        """Fetch a new bearer token for use with the OTel collector."""

        try:
            bearer_token_response = cast(
                auth_pb2.GetBearerTokenResponse,
                self.__auth_service.GetBearerToken(
                    metadata=self.config.metadata,
                    request=auth_pb2.GetBearerTokenRequest(
                        environment=self.config.environment,
                    ),
                    timeout=DEFAULT_TIMEOUT,
                ),
            )
            return bearer_token_response.bearer_token
        except grpc.RpcError as rpc_error:
            logging.debug(str(rpc_error))
            return ""

    async def connect_otel(self):
        """Connect to OTEL collector and create global meter and tracer."""

        if os.environ.get("STANZA_NO_OTEL"):
            # Skip connecting OTEL if STANZA_NO_OTEL environment variable exists.
            return

        if self.__service_config:
            bearer_token = await self.fetch_otel_bearer_token()
            if bearer_token:
                otel = OpenTelemetry(
                    bearer_token=bearer_token,
                    metric_collector_url=self.__service_config.metric_config.collector_url,
                    trace_collector_url=self.__service_config.trace_config.collector_url,
                    trace_sample_rate=self.__service_config.trace_config.sample_rate_default,
                    service_name=str(self.config.service_name or ""),
                    service_release=str(self.config.service_release or ""),
                    environment=str(self.config.environment or ""),
                )
                if otel.new_meter() and otel.new_tracer():
                    self.__otel = otel

    async def fetch_service_config(self):
        """Fetch service configuration changes."""

        with service_config_lock:
            last_version = self.__service_config
            last_version_seen = self.__service_config_version

            try:
                service_config_response = cast(
                    config_pb2.GetServiceConfigResponse,
                    self.__config_service.GetServiceConfig(
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
                        timeout=DEFAULT_TIMEOUT,
                    ),
                )
            except grpc.RpcError as rpc_error:
                logging.debug(str(rpc_error))
                return

            if service_config_response.config_data_sent:
                self.__service_config = service_config_response.config
                self.__service_config_version = service_config_response.version
                self.config.customer_id = service_config_response.config.customer_id
                logging.debug(
                    "Service config has changed from version '%s' to '%s'",
                    last_version_seen,
                    service_config_response.version,
                )

                if (
                    not self.__otel
                    or not last_version
                    or (
                        last_version.trace_config
                        != service_config_response.config.trace_config
                        or last_version.metric_config
                        != service_config_response.config.metric_config
                    )
                ):
                    await self.connect_otel()

    async def fetch_guard_config(
        self, guard_name: str
    ) -> (tuple[config_pb2.GuardConfig, common_pb2.Config]):
        """Fetch guard configuration changes for a specific guard."""

        with guard_config_locks[guard_name]:
            existing_guard_config = self.__guard_configs.get(guard_name)
            last_version_seen = None
            if existing_guard_config:
                last_version_seen = existing_guard_config["version"]

            try:
                guard_config_response = cast(
                    config_pb2.GetGuardConfigResponse,
                    self.__config_service.GetGuardConfig(
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
                        timeout=DEFAULT_TIMEOUT,
                    ),
                )
            except grpc.RpcError as rpc_error:
                logging.debug(str(rpc_error))
                return config_pb2.GuardConfig(), common_pb2.Config.CONFIG_FETCH_ERROR

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
                return config_pb2.GuardConfig(), common_pb2.Config.CONFIG_FETCHED_OK

    async def refetch_known_guard_configs(self):
        """Refetch all known instantiated guards."""

        tasks = [
            asyncio.create_task(self.fetch_guard_config(guard_name))
            for guard_name in self.__guard_configs
        ]
        if len(tasks) > 0:
            await asyncio.wait(tasks)
