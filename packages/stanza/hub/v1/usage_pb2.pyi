from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from stanza.hub.v1 import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QueryMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    QUERY_MODE_UNSPECIFIED: _ClassVar[QueryMode]
    QUERY_MODE_SUM: _ClassVar[QueryMode]
    QUERY_MODE_REPORT: _ClassVar[QueryMode]
QUERY_MODE_UNSPECIFIED: QueryMode
QUERY_MODE_SUM: QueryMode
QUERY_MODE_REPORT: QueryMode

class GetUsageRequest(_message.Message):
    __slots__ = ("environment", "guard", "guard_query_mode", "start_ts", "end_ts", "apikey", "feature", "feature_query_mode", "service", "service_query_mode", "priority", "priority_query_mode", "report_tags", "tags", "report_all_tags", "step")
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    GUARD_FIELD_NUMBER: _ClassVar[int]
    GUARD_QUERY_MODE_FIELD_NUMBER: _ClassVar[int]
    START_TS_FIELD_NUMBER: _ClassVar[int]
    END_TS_FIELD_NUMBER: _ClassVar[int]
    APIKEY_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FIELD_NUMBER: _ClassVar[int]
    FEATURE_QUERY_MODE_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    SERVICE_QUERY_MODE_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_QUERY_MODE_FIELD_NUMBER: _ClassVar[int]
    REPORT_TAGS_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    REPORT_ALL_TAGS_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    environment: str
    guard: str
    guard_query_mode: QueryMode
    start_ts: _timestamp_pb2.Timestamp
    end_ts: _timestamp_pb2.Timestamp
    apikey: str
    feature: str
    feature_query_mode: QueryMode
    service: str
    service_query_mode: QueryMode
    priority: int
    priority_query_mode: QueryMode
    report_tags: _containers.RepeatedScalarFieldContainer[str]
    tags: _containers.RepeatedCompositeFieldContainer[_common_pb2.Tag]
    report_all_tags: bool
    step: str
    def __init__(self, environment: _Optional[str] = ..., guard: _Optional[str] = ..., guard_query_mode: _Optional[_Union[QueryMode, str]] = ..., start_ts: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_ts: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., apikey: _Optional[str] = ..., feature: _Optional[str] = ..., feature_query_mode: _Optional[_Union[QueryMode, str]] = ..., service: _Optional[str] = ..., service_query_mode: _Optional[_Union[QueryMode, str]] = ..., priority: _Optional[int] = ..., priority_query_mode: _Optional[_Union[QueryMode, str]] = ..., report_tags: _Optional[_Iterable[str]] = ..., tags: _Optional[_Iterable[_Union[_common_pb2.Tag, _Mapping]]] = ..., report_all_tags: bool = ..., step: _Optional[str] = ...) -> None: ...

class GetUsageResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: _containers.RepeatedCompositeFieldContainer[UsageTimeseries]
    def __init__(self, result: _Optional[_Iterable[_Union[UsageTimeseries, _Mapping]]] = ...) -> None: ...

class UsageTimeseries(_message.Message):
    __slots__ = ("data", "feature", "priority", "tags", "guard", "service")
    DATA_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    GUARD_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[UsageTSDataPoint]
    feature: str
    priority: int
    tags: _containers.RepeatedCompositeFieldContainer[_common_pb2.Tag]
    guard: str
    service: str
    def __init__(self, data: _Optional[_Iterable[_Union[UsageTSDataPoint, _Mapping]]] = ..., feature: _Optional[str] = ..., priority: _Optional[int] = ..., tags: _Optional[_Iterable[_Union[_common_pb2.Tag, _Mapping]]] = ..., guard: _Optional[str] = ..., service: _Optional[str] = ...) -> None: ...

class UsageTSDataPoint(_message.Message):
    __slots__ = ("start_ts", "end_ts", "granted", "granted_weight", "not_granted", "not_granted_weight", "be_burst", "be_burst_weight", "parent_reject", "parent_reject_weight")
    START_TS_FIELD_NUMBER: _ClassVar[int]
    END_TS_FIELD_NUMBER: _ClassVar[int]
    GRANTED_FIELD_NUMBER: _ClassVar[int]
    GRANTED_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    NOT_GRANTED_FIELD_NUMBER: _ClassVar[int]
    NOT_GRANTED_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    BE_BURST_FIELD_NUMBER: _ClassVar[int]
    BE_BURST_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    PARENT_REJECT_FIELD_NUMBER: _ClassVar[int]
    PARENT_REJECT_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    start_ts: _timestamp_pb2.Timestamp
    end_ts: _timestamp_pb2.Timestamp
    granted: int
    granted_weight: float
    not_granted: int
    not_granted_weight: float
    be_burst: int
    be_burst_weight: float
    parent_reject: int
    parent_reject_weight: float
    def __init__(self, start_ts: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_ts: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., granted: _Optional[int] = ..., granted_weight: _Optional[float] = ..., not_granted: _Optional[int] = ..., not_granted_weight: _Optional[float] = ..., be_burst: _Optional[int] = ..., be_burst_weight: _Optional[float] = ..., parent_reject: _Optional[int] = ..., parent_reject_weight: _Optional[float] = ...) -> None: ...
