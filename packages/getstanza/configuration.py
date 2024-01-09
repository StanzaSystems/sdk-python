import datetime
import os
import uuid
from typing import Optional

CONFIG_POLL_INTERVAL_SECS = 15


class StanzaConfiguration:
    """
    Stanza SDK configuration. Values can be set directly as parameters to the
    constructor, and when not present, are pulled from the environment.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        service_name: Optional[str] = None,
        service_release: Optional[str] = None,
        environment: Optional[str] = None,
        hub_address: Optional[str] = None,
    ):
        if not api_key:
            if os.environ.get("STANZA_API_KEY"):
                self.api_key = os.environ.get("STANZA_API_KEY")
            else:
                raise ValueError(
                    "Missing required Stanza API key "
                    "(Hint: Set a STANZA_API_KEY environment variable!)"
                )
        else:
            self.api_key = api_key

        if not service_name:
            if os.environ.get("STANZA_SERVICE_NAME"):
                self.service_name = os.environ.get("STANZA_SERVICE_NAME")
            else:
                raise ValueError(
                    "Missing required service name "
                    "(Hint: Set a STANZA_SERVICE_NAME environment variable!)"
                )
        else:
            self.service_name = service_name

        if not service_release:
            if os.environ.get("STANZA_SERVICE_RELEASE"):
                self.service_release = os.environ.get("STANZA_SERVICE_RELEASE")
            else:
                self.service_release = "0.0.0"
        else:
            self.service_release = service_release

        if not environment:
            if os.environ.get("STANZA_ENVIRONMENT"):
                self.environment = os.environ.get("STANZA_ENVIRONMENT")
            else:
                self.environment = "dev"
        else:
            self.environment = environment

        if not hub_address:
            if os.environ.get("STANZA_HUB_ADDRESS"):
                self.hub_address = os.environ.get("STANZA_HUB_ADDRESS")
            else:
                self.hub_address = "hub.stanzasys.co:9020"
        else:
            self.hub_address = hub_address

        self.interval = datetime.timedelta(seconds=CONFIG_POLL_INTERVAL_SECS)
        self.client_id = str(uuid.uuid4())
        self.customer_id: Optional[str] = None
        self.metadata = [("x-stanza-key", self.api_key)]
