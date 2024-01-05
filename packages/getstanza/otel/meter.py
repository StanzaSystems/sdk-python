# import os
from typing import Dict, Optional

from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.metrics import Meter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    MetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry.sdk.resources import Resource

# Constants per Stanza SDK spec
METRIC_EXPORT_INTERVAL = 10_000  # 10,000 milliseconds = 10 seconds
METRIC_EXPORT_TIMEOUT = 30_000  # 30,000 milliseconds = 30 seconds


class StanzaMeter:
    def __init__(self, meter: Meter):
        self.AllowedCount = meter.create_counter(
            name="stanza.guard.allowed",
            unit="1",
            description="measures the number of executions that were allowed",
        )
        self.AllowedSuccessCount = meter.create_counter(
            name="stanza.guard.allowed.success",
            unit="1",
            description="measures the number of executions that succeeded",
        )
        self.AllowedFailureCount = meter.create_counter(
            name="stanza.guard.allowed.failure",
            unit="1",
            description="measures the number of executions that failed",
        )
        self.AllowedUnknownCount = meter.create_counter(
            name="stanza.guard.allowed.unknown",
            unit="1",
            description="measures the number of executions where the success (or failure) was unknown",
        )
        self.AllowedDuration = meter.create_histogram(
            name="stanza.guard.allowed.duration",
            unit="ms",
            description="measures the total executions time of guarded requests",
        )
        self.BlockedCount = meter.create_counter(
            name="stanza.guard.blocked",
            unit="1",
            description="measures the number of executions that were backpressured",
        )
        self.FailOpenCount = meter.create_counter(
            name="stanza.guard.failopen",
            unit="1",
            description="measures the number of executions that failed open",
        )


class StanzaMeterProvider:
    @property
    def provider(self):
        return self.__provider

    def __init__(
        self,
        debug: bool,
        insecure: bool,
        resource: Resource,
        endpoint: str,
        headers: Dict[str, str],
    ):
        if debug:
            exporter = self.__debug_meter_provider()
        else:
            exporter = self.__grpc_meter_provider(endpoint, insecure, headers)

        self.__provider = MeterProvider(
            metric_readers=[
                PeriodicExportingMetricReader(
                    exporter=exporter,
                    export_interval_millis=METRIC_EXPORT_INTERVAL,
                    export_timeout_millis=METRIC_EXPORT_TIMEOUT,
                )
            ],
            resource=resource,
        )

    def __debug_meter_provider(self) -> MetricExporter:
        return ConsoleMetricExporter()

    def __grpc_meter_provider(
        self, endpoint: str, insecure: bool, headers: Dict[str, str]
    ) -> MetricExporter:
        return OTLPMetricExporter(
            endpoint=endpoint,
            insecure=insecure,
            # credentials=  # TODO: allow passing credentials
            headers=headers,
            # timeout= # TODO: how is this timeout different from export_timeout_millis?
        )

    def get_meter(
        self, name: str, version: str, schema_url: Optional[str] = None
    ) -> StanzaMeter:
        return StanzaMeter(
            self.__provider.get_meter(name=name, version=version, schema_url=schema_url)
        )
