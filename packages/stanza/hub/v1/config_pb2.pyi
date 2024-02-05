from google.api import annotations_pb2 as _annotations_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from stanza.hub.v1 import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetGuardConfigRequest(_message.Message):
    __slots__ = ("version_seen", "selector")
    VERSION_SEEN_FIELD_NUMBER: _ClassVar[int]
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    version_seen: str
    selector: _common_pb2.GuardServiceSelector
    def __init__(self, version_seen: _Optional[str] = ..., selector: _Optional[_Union[_common_pb2.GuardServiceSelector, _Mapping]] = ...) -> None: ...

class GetGuardConfigResponse(_message.Message):
    __slots__ = ("version", "config_data_sent", "config")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    CONFIG_DATA_SENT_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    version: str
    config_data_sent: bool
    config: GuardConfig
    def __init__(self, version: _Optional[str] = ..., config_data_sent: bool = ..., config: _Optional[_Union[GuardConfig, _Mapping]] = ...) -> None: ...

class GuardConfig(_message.Message):
    __slots__ = ("validate_ingress_tokens", "check_quota", "quota_tags", "report_only")
    VALIDATE_INGRESS_TOKENS_FIELD_NUMBER: _ClassVar[int]
    CHECK_QUOTA_FIELD_NUMBER: _ClassVar[int]
    QUOTA_TAGS_FIELD_NUMBER: _ClassVar[int]
    REPORT_ONLY_FIELD_NUMBER: _ClassVar[int]
    validate_ingress_tokens: bool
    check_quota: bool
    quota_tags: _containers.RepeatedScalarFieldContainer[str]
    report_only: bool
    def __init__(self, validate_ingress_tokens: bool = ..., check_quota: bool = ..., quota_tags: _Optional[_Iterable[str]] = ..., report_only: bool = ...) -> None: ...

class GetBrowserContextRequest(_message.Message):
    __slots__ = ("feature",)
    FEATURE_FIELD_NUMBER: _ClassVar[int]
    feature: _common_pb2.FeatureSelector
    def __init__(self, feature: _Optional[_Union[_common_pb2.FeatureSelector, _Mapping]] = ...) -> None: ...

class GetBrowserContextResponse(_message.Message):
    __slots__ = ("feature_configs",)
    FEATURE_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    feature_configs: _containers.RepeatedCompositeFieldContainer[FeatureConfig]
    def __init__(self, feature_configs: _Optional[_Iterable[_Union[FeatureConfig, _Mapping]]] = ...) -> None: ...

class FeatureConfig(_message.Message):
    __slots__ = ("name", "config")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    name: str
    config: BrowserConfig
    def __init__(self, name: _Optional[str] = ..., config: _Optional[_Union[BrowserConfig, _Mapping]] = ...) -> None: ...

class BrowserConfig(_message.Message):
    __slots__ = ("enabled_percent", "action_code_enabled", "message_enabled", "action_code_disabled", "message_disabled")
    ENABLED_PERCENT_FIELD_NUMBER: _ClassVar[int]
    ACTION_CODE_ENABLED_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ACTION_CODE_DISABLED_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_DISABLED_FIELD_NUMBER: _ClassVar[int]
    enabled_percent: int
    action_code_enabled: int
    message_enabled: str
    action_code_disabled: int
    message_disabled: str
    def __init__(self, enabled_percent: _Optional[int] = ..., action_code_enabled: _Optional[int] = ..., message_enabled: _Optional[str] = ..., action_code_disabled: _Optional[int] = ..., message_disabled: _Optional[str] = ...) -> None: ...

class GetServiceConfigRequest(_message.Message):
    __slots__ = ("version_seen", "service", "client_id")
    VERSION_SEEN_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    version_seen: str
    service: _common_pb2.ServiceSelector
    client_id: str
    def __init__(self, version_seen: _Optional[str] = ..., service: _Optional[_Union[_common_pb2.ServiceSelector, _Mapping]] = ..., client_id: _Optional[str] = ...) -> None: ...

class GetServiceConfigResponse(_message.Message):
    __slots__ = ("version", "config_data_sent", "config")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    CONFIG_DATA_SENT_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    version: str
    config_data_sent: bool
    config: ServiceConfig
    def __init__(self, version: _Optional[str] = ..., config_data_sent: bool = ..., config: _Optional[_Union[ServiceConfig, _Mapping]] = ...) -> None: ...

class ServiceConfig(_message.Message):
    __slots__ = ("customer_id", "trace_config", "metric_config", "sentinel_config")
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    TRACE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    METRIC_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SENTINEL_CONFIG_FIELD_NUMBER: _ClassVar[int]
    customer_id: str
    trace_config: TraceConfig
    metric_config: MetricConfig
    sentinel_config: SentinelConfig
    def __init__(self, customer_id: _Optional[str] = ..., trace_config: _Optional[_Union[TraceConfig, _Mapping]] = ..., metric_config: _Optional[_Union[MetricConfig, _Mapping]] = ..., sentinel_config: _Optional[_Union[SentinelConfig, _Mapping]] = ...) -> None: ...

class TraceConfig(_message.Message):
    __slots__ = ("collector_url", "sample_rate_default", "overrides", "header_sample_configs", "param_sample_configs")
    COLLECTOR_URL_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_RATE_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    OVERRIDES_FIELD_NUMBER: _ClassVar[int]
    HEADER_SAMPLE_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    PARAM_SAMPLE_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    collector_url: str
    sample_rate_default: float
    overrides: _containers.RepeatedCompositeFieldContainer[TraceConfigOverride]
    header_sample_configs: _containers.RepeatedCompositeFieldContainer[HeaderTraceConfig]
    param_sample_configs: _containers.RepeatedCompositeFieldContainer[ParamTraceConfig]
    def __init__(self, collector_url: _Optional[str] = ..., sample_rate_default: _Optional[float] = ..., overrides: _Optional[_Iterable[_Union[TraceConfigOverride, _Mapping]]] = ..., header_sample_configs: _Optional[_Iterable[_Union[HeaderTraceConfig, _Mapping]]] = ..., param_sample_configs: _Optional[_Iterable[_Union[ParamTraceConfig, _Mapping]]] = ...) -> None: ...

class MetricConfig(_message.Message):
    __slots__ = ("collector_url",)
    COLLECTOR_URL_FIELD_NUMBER: _ClassVar[int]
    collector_url: str
    def __init__(self, collector_url: _Optional[str] = ...) -> None: ...

class SentinelConfig(_message.Message):
    __slots__ = ("circuitbreaker_rules_json", "flow_rules_json", "isolation_rules_json", "system_rules_json")
    CIRCUITBREAKER_RULES_JSON_FIELD_NUMBER: _ClassVar[int]
    FLOW_RULES_JSON_FIELD_NUMBER: _ClassVar[int]
    ISOLATION_RULES_JSON_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_RULES_JSON_FIELD_NUMBER: _ClassVar[int]
    circuitbreaker_rules_json: str
    flow_rules_json: str
    isolation_rules_json: str
    system_rules_json: str
    def __init__(self, circuitbreaker_rules_json: _Optional[str] = ..., flow_rules_json: _Optional[str] = ..., isolation_rules_json: _Optional[str] = ..., system_rules_json: _Optional[str] = ...) -> None: ...

class TraceConfigOverride(_message.Message):
    __slots__ = ("sample_rate", "span_selectors")
    SAMPLE_RATE_FIELD_NUMBER: _ClassVar[int]
    SPAN_SELECTORS_FIELD_NUMBER: _ClassVar[int]
    sample_rate: float
    span_selectors: _containers.RepeatedCompositeFieldContainer[SpanSelector]
    def __init__(self, sample_rate: _Optional[float] = ..., span_selectors: _Optional[_Iterable[_Union[SpanSelector, _Mapping]]] = ...) -> None: ...

class SpanSelector(_message.Message):
    __slots__ = ("otel_attribute", "value")
    OTEL_ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    otel_attribute: str
    value: str
    def __init__(self, otel_attribute: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class HeaderTraceConfig(_message.Message):
    __slots__ = ("span_selectors", "request_header_names", "response_header_names")
    SPAN_SELECTORS_FIELD_NUMBER: _ClassVar[int]
    REQUEST_HEADER_NAMES_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_HEADER_NAMES_FIELD_NUMBER: _ClassVar[int]
    span_selectors: _containers.RepeatedCompositeFieldContainer[SpanSelector]
    request_header_names: _containers.RepeatedScalarFieldContainer[str]
    response_header_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, span_selectors: _Optional[_Iterable[_Union[SpanSelector, _Mapping]]] = ..., request_header_names: _Optional[_Iterable[str]] = ..., response_header_names: _Optional[_Iterable[str]] = ...) -> None: ...

class ParamTraceConfig(_message.Message):
    __slots__ = ("span_selectors", "parameter_names")
    SPAN_SELECTORS_FIELD_NUMBER: _ClassVar[int]
    PARAMETER_NAMES_FIELD_NUMBER: _ClassVar[int]
    span_selectors: _containers.RepeatedCompositeFieldContainer[SpanSelector]
    parameter_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, span_selectors: _Optional[_Iterable[_Union[SpanSelector, _Mapping]]] = ..., parameter_names: _Optional[_Iterable[str]] = ...) -> None: ...
