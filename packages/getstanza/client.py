import logging

from getstanza.configuration import StanzaConfiguration
from getstanza.configuration_manager import StanzaConfigurationManager
from getstanza.hub_poller import StanzaHubPoller


class StanzaClient:
    """
    SDK client that assists with integrating with Hub and managing the active
    service and guard configurations.
    """

    def __init__(self, config: StanzaConfiguration):
        self.config = config
        self.config_manager = StanzaConfigurationManager(config)
        self.hub_poller = StanzaHubPoller(
            config_manager=self.config_manager,
            interval=config.interval,
        )

        # TODO: Initialize OTEL TextMapPropagator here
        # otel.InitTextMapPropagator(otel.StanzaHeaders{})

        # TODO: Consider allowing this all to be setup on another thread so this
        # works well with synchronous frameworks like Flask?

    def init(self):
        """Use to initialize the Stanza SDK."""

        logging.debug("Initializing Stanza")

        self.hub_poller.start()
