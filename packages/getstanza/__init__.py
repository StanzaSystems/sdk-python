"""
Python SDK for adding Stanza Systems fault tolerance to your Python 3 service.
"""

import datetime
import logging
import os
from typing import Optional

from getstanza.configuration_manager import StanzaConfigurationManager
from getstanza.hub_poller import StanzaHubPoller


def init(
    api_key: Optional[str] = None,
    service_name: Optional[str] = None,
    service_release: Optional[str] = None,
    service_environment: Optional[str] = None,
    hub_address: Optional[str] = None,
):
    """Use to initialize Stanza SDK"""

    logging.debug("Initializing Stanza")

    if not api_key:
        if os.environ.get("STANZA_API_KEY"):
            api_key = os.environ.get("STANZA_API_KEY")
        else:
            raise ValueError(
                "Missing required Stanza API key (Hint: Set a STANZA_API_KEY environment variable!)"
            )

    if not service_name:
        if os.environ.get("STANZA_SERVICE_NAME"):
            service_name = os.environ.get("STANZA_SERVICE_NAME")
        else:
            service_name = "unknown_service"

    if not service_release:
        if os.environ.get("STANZA_SERVICE_RELEASE"):
            service_release = os.environ.get("STANZA_SERVICE_RELEASE")
        else:
            service_release = "0.0.0"

    if not service_environment:
        if os.environ.get("STANZA_ENVIRONMENT"):
            service_release = os.environ.get("STANZA_ENVIRONMENT")
        else:
            service_release = "unknown"

    if not hub_address:
        if os.environ.get("STANZA_HUB_ADDRESS"):
            hub_address = os.environ.get("STANZA_HUB_ADDRESS")
        else:
            hub_address = "https://hub.stanzasys.co"

    # TODO: Initialize OTEL TextMapPropagator here
    # otel.InitTextMapPropagator(otel.StanzaHeaders{})

    # TODO: Consider allowing this all to be setup on another thread?

    configuration_manager = StanzaConfigurationManager(
        api_key=api_key,
        service_name=service_name,
        service_release=service_release,
        environment=service_environment,
        hub_address=hub_address,
    )

    # TODO: Before PR make sure to make it not stop looping on network failure.
    hub_poller = StanzaHubPoller(
        configuration_manager=configuration_manager,
        interval=datetime.timedelta(seconds=15),
    )
    hub_poller.begin()
