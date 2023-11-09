import json
import logging
import uuid
from typing import MutableMapping, Optional

import requests
from getstanza import hub
from getstanza.errors.hub import hub_error


class StanzaConfigurationManager:
    """State manager for the active service configuration."""

    def __init__(
        self,
        api_key: str,
        service_name: str,
        service_release: str,
        environment: str,
        hub_address: str,
    ):
        self.api_key = api_key
        self.service_name = service_name
        self.release = service_release
        self.environment = environment
        self.hub_address = hub_address
        self.client_id = str(uuid.uuid4())

        # TODO: There's a couple of things to note here.
        #
        # 1. Consider re-creating the API client whenever attributes it depends on change.
        # 2. Configure a reasonable default timeout. This specific generated
        # client is going to be replaced soon, so that's unhandled as of now.
        self.__hub_conn = hub.RemoteCaller(
            url_prefix=hub_address, headers={"X-Stanza-Key": api_key}
        )

        # TODO: Utilize type aliases whenever we upgrade to Python 3.12.
        self.__service_config: Optional[hub.V1ServiceConfig] = None
        self.__service_config_version: Optional[str] = None
        self.__guard_configs: MutableMapping[str, tuple[str, hub.V1GuardConfig]] = {}
        self.__bearer_token: Optional[str] = None

        # TODO: Add refetch logic for this whenever 'exp' happens.
        self.fetch_otel_bearer_token()

    def get_guard_config(self, guard_name: str) -> Optional[hub.V1GuardConfig]:
        """Retrieves the guard config for a specified guard."""

        return (
            self.__guard_configs[guard_name][1]
            if guard_name in self.__guard_configs
            else None
        )

    def fetch_otel_bearer_token(self):
        """Fetch a new bearer token for use with the OTel collector."""

        try:
            bearer_token_response = self.__hub_conn.auth_service_get_bearer_token(
                environment=self.environment
            )
            self.__bearer_token = bearer_token_response.bearer_token
        except requests.exceptions.HTTPError as exc:
            raise hub_error(exc) from exc

    def fetch_service_config(self):
        """Fetch service configuration changes."""

        try:
            service_config_response = self.__hub_conn.config_service_get_service_config(
                hub.V1GetServiceConfigRequest(
                    version_seen=self.__service_config_version,
                    service=hub.V1ServiceSelector(
                        environment=self.environment,
                        name=self.service_name,
                        release=self.release,
                    ),
                    client_id=self.client_id,
                )
            )
        except requests.exceptions.HTTPError as exc:
            raise hub_error(exc) from exc

        if service_config_response.version != self.__service_config_version:
            self.__service_config = service_config_response.config
            self.__service_config_version = service_config_response.version

            logging.debug(
                "Service config has changed from version '%s' to '%s'",
                service_config_response.version,
                self.__service_config_version,
            )
            logging.debug(
                "New active service config: %s",
                json.dumps(
                    self.__service_config.to_jsonable(), indent=2, sort_keys=True
                ),
            )

    def fetch_guard_config(self, guard_name: str):
        """Refetch guard configuration changes for a specific guard."""

        existing_guard_config = self.__guard_configs.get(guard_name)
        last_version_seen = existing_guard_config and existing_guard_config[0]

        try:
            guard_config_response = self.__hub_conn.config_service_get_guard_config(
                hub.V1GetGuardConfigRequest(
                    version_seen=last_version_seen,
                    selector=hub.V1GuardServiceSelector(
                        environment=self.environment,
                        guard_name=guard_name,
                        service_name=self.service_name,
                        service_release=self.release,
                    ),
                )
            )
        except requests.exceptions.HTTPError as exc:
            raise hub_error(exc) from exc

        if last_version_seen != guard_config_response.version:
            self.__guard_configs[guard_name] = (
                guard_config_response.version,
                guard_config_response.config,
            )

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
                    guard_config_response.config.to_jsonable(),
                    indent=2,
                    sort_keys=True,
                ),
            )

    def refetch_known_guard_configs(self):
        """Refetch all known instantiated guards."""

        # TODO: Make asyncio friendly once generated API library is replaced.
        for guard_name in self.__guard_configs:
            self.fetch_guard_config(guard_name)
