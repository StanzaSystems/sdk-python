# import os
from typing import Dict, Optional

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SpanExporter,
)
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased
from opentelemetry.trace import Tracer

# Constants per Stanza SDK spec
TRACE_EXPORT_INTERVAL = 10_000  # 10,000 milliseconds = 10 seconds
TRACE_EXPORT_TIMEOUT = 30_000  # 30,000 milliseconds = 30 seconds


class StanzaTracerProvider:
    @property
    def provider(self):
        return self.__provider

    def __init__(
        self,
        debug: bool,
        insecure: bool,
        resource: Resource,
        sampler: TraceIdRatioBased,
        endpoint: str,
        headers: Dict[str, str],
    ):
        if debug:
            exporter = self.__debug_span_exporter()
        else:
            exporter = self.__grpc_span_exporter(endpoint, insecure, headers)
        self.__provider = TracerProvider(resource=resource, sampler=sampler)
        self.__provider.add_span_processor(
            BatchSpanProcessor(
                span_exporter=exporter,
                schedule_delay_millis=TRACE_EXPORT_INTERVAL,
                export_timeout_millis=TRACE_EXPORT_TIMEOUT,
            )
        )

    def __debug_span_exporter(self) -> SpanExporter:
        return ConsoleSpanExporter()

    def __grpc_span_exporter(
        self, endpoint: str, insecure: bool, headers: Dict[str, str]
    ) -> SpanExporter:
        return OTLPSpanExporter(
            endpoint=endpoint,
            insecure=insecure,
            # credentials=  # TODO: allow passing credentials
            headers=headers,
            # timeout= # TODO: how is this timeout different from export_timeout_millis?
        )

    def get_tracer(
        self, name: str, version: str, schema_url: Optional[str] = None
    ) -> Tracer:
        return self.__provider.get_tracer(
            instrumenting_module_name=name,
            instrumenting_library_version=version,
            schema_url=schema_url,
        )
