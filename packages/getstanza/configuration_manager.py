import json
import logging
import uuid
from typing import MutableMapping, Optional

import requests
from getstanza import hub
from getstanza.errors import hub_error


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

        # TODO: Re-create this caller whenever attributes it depends on change.
        self.hub_conn = hub.RemoteCaller(
            url_prefix=hub_address, headers={"X-Stanza-Key": api_key}
        )

        # TODO: Utilize type aliases whenever we upgrade to Python 3.12.
        self.service_config: Optional[hub.V1ServiceConfig] = None
        self.service_config_version: Optional[str] = None
        self.guard_configs: MutableMapping[str, tuple[str, hub.V1GuardConfig]] = {}
        self.bearer_token: Optional[str] = None

        # TODO: Add refetch logic for this whenever 'exp' happens.
        self.fetch_otel_bearer_token()

    def fetch_otel_bearer_token(self):
        """Fetch a new bearer token for use with the OTel collector."""

        try:
            bearer_token_response = self.hub_conn.auth_service_get_bearer_token(
                environment=self.environment
            )
            self.bearer_token = bearer_token_response.bearer_token
        except requests.exceptions.HTTPError as exc:
            raise hub_error(exc) from exc

    def fetch_service_config(self):
        """Poll for service configuration changes."""

        try:
            service_config_response = self.hub_conn.config_service_get_service_config(
                hub.V1GetServiceConfigRequest(
                    version_seen=self.service_config_version,
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

        if service_config_response.version != self.service_config_version:
            self.service_config = service_config_response.config
            self.service_config_version = service_config_response.version

            logging.debug(
                "Service config has changed from version '%s' to '%s'",
                service_config_response.version,
                self.service_config_version,
            )
            logging.debug(
                "New active service config: %s",
                json.dumps(self.service_config.to_jsonable(), indent=2, sort_keys=True),
            )

    def fetch_guard_config(self, guard_name: str):
        """Poll for guard configuration changes."""

        existing_guard_config = self.guard_configs.get(guard_name)
        last_version_seen = existing_guard_config and existing_guard_config[0]

        try:
            guard_config_response = self.hub_conn.config_service_get_guard_config(
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
            self.guard_configs[guard_name] = (
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
