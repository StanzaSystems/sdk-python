import logging
import os
from typing import cast

# from getstanza.configuration import StanzaConfiguration
import getstanza.client
from getstanza.otel.meter import StanzaMeterProvider
from getstanza.otel.tracer import StanzaTracerProvider
from opentelemetry.metrics import Meter
from opentelemetry.sdk.resources import Resource
from opentelemetry.trace import Tracer

INSTRUMENTATION_NAME = "github.com/StanzaSystems/sdk-python"
INSTRUMENTATION_VERSION = "0.0.1-beta"


class OpenTelemetry:
    """Implements OTEL metrics and traces."""

    @property
    def meter(self) -> Meter:
        return self.__meter

    @property
    def tracer(self) -> Tracer:
        return self.__tracer

    def __init__(
        self, bearer_token: str, metric_collector_url: str, trace_collector_url: str
    ):
        client = getstanza.client.StanzaClient.getInstance()

        self.__debug = False
        self.__insecure = False
        self.__metric_collector_url = metric_collector_url
        self.__trace_collector_url = trace_collector_url

        if os.environ.get("STANZA_OTEL_DEBUG"):
            self.__debug = True
            self.__insecure = True

        if os.environ.get("STANZA_OTEL_INSECURE"):
            self.__insecure = True

        # TODO: Fetch bearer token here instead of passing it in?
        self.__bearer_token = bearer_token

        # Define shared OpenTelemetry resource.
        # https://opentelemetry.io/docs/specs/otel/resource/sdk/
        self.__resource = Resource.create(
            {
                "service.name": cast(str, client.config.service_name),
                "service.version": cast(str, client.config.service_release),
                "deployment.environment": cast(str, client.config.environment),
            }
        )

    def new_meter(self) -> bool:
        """Setup OpenTelemetry meter provider and create new meter."""
        try:
            self.__meter_provider = StanzaMeterProvider(
                self.__debug,
                self.__insecure,
                resource=self.__resource,
                endpoint=self.__metric_collector_url,
                headers={"Authorization": "Bearer " + self.__bearer_token},
            )
            self.__meter = self.__meter_provider.get_meter(
                INSTRUMENTATION_NAME, INSTRUMENTATION_VERSION
            )
            return True
        except Exception as exc:
            # TODO: add real/better exception handling
            logging.exception(exc)
            return False

    def new_tracer(self) -> bool:
        """Setup OpenTelemetry trace provider."""
        try:
            self.__trace_provider = StanzaTracerProvider(
                debug=self.__debug,
                insecure=self.__insecure,
                resource=self.__resource,
                endpoint=self.__trace_collector_url,
                headers={"Authorization": "Bearer " + self.__bearer_token},
            )
            self.__tracer = self.__trace_provider.get_tracer(
                INSTRUMENTATION_NAME, INSTRUMENTATION_VERSION
            )
            return True
        except Exception as exc:
            # TODO: add real/better exception handling
            logging.exception(exc)
            return False
