"""
Python SDK for adding Stanza Systems fault tolerance to your python 3 service.
"""

import logging
import os
from typing import Optional


def init(
    api_key: Optional[str] = None,
    service_name: Optional[str] = None,
    service_release: Optional[str] = None,
    service_environment: Optional[str] = None,
    hub_address: Optional[str] = None,
):
    """Use to initialize Stanza SDK"""
    logging.debug("Initializing Stanza")

    if api_key is None or api_key == "":
        if os.environ.get("STANZA_API_KEY") != "":
            api_key = os.environ.get("STANZA_API_KEY")
        else:
            logging.error(
                "missing required Stanza API key (Hint: Set a STANZA_API_KEY environment variable!)"
            )
            return

    if service_name is None or service_name == "":
        if os.environ.get("STANZA_SERVICE_NAME") != "":
            service_name = os.environ.get("STANZA_SERVICE_NAME")
        else:
            service_name = "unknown_service"

    if service_release is None or service_release == "":
        if os.environ.get("STANZA_SERVICE_RELEASE") != "":
            service_release = os.environ.get("STANZA_SERVICE_RELEASE")
        else:
            service_release = "0.0.0"

    if service_environment is None or service_environment == "":
        if os.environ.get("STANZA_ENVIRONMENT") != "":
            service_release = os.environ.get("STANZA_ENVIRONMENT")
        else:
            service_release = "unknown"

    if hub_address is None or hub_address == "":
        if os.environ.get("STANZA_HUB_ADDRESS") != "":
            hub_address = os.environ.get("STANZA_HUB_ADDRESS")
        else:
            hub_address = "https://hub.stanzasys.co"

    # TODO: Initialize OTEL TextMapPropagator here
    # otel.InitTextMapPropagator(otel.StanzaHeaders{})

    # TODO: Initialize new global stanza state here
    # global.NewState()
