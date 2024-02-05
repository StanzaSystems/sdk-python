from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from stanza.hub.v1 import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UpdateStreamsRequest(_message.Message):
    __slots__ = ("guard_name", "environment", "requests", "ended")
    GUARD_NAME_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    ENDED_FIELD_NUMBER: _ClassVar[int]
    guard_name: str
    environment: str
    requests: _containers.RepeatedCompositeFieldContainer[StreamRequest]
    ended: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, guard_name: _Optional[str] = ..., environment: _Optional[str] = ..., requests: _Optional[_Iterable[_Union[StreamRequest, _Mapping]]] = ..., ended: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdateStreamsResponse(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[StreamResult]
    def __init__(self, results: _Optional[_Iterable[_Union[StreamResult, _Mapping]]] = ...) -> None: ...

class StreamRequest(_message.Message):
    __slots__ = ("feature", "tags", "priority_boost", "stream_id", "max_weight", "min_weight")
    FEATURE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_BOOST_FIELD_NUMBER: _ClassVar[int]
    STREAM_ID_FIELD_NUMBER: _ClassVar[int]
    MAX_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    MIN_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    feature: str
    tags: _containers.RepeatedCompositeFieldContainer[_common_pb2.Tag]
    priority_boost: int
    stream_id: str
    max_weight: float
    min_weight: float
    def __init__(self, feature: _Optional[str] = ..., tags: _Optional[_Iterable[_Union[_common_pb2.Tag, _Mapping]]] = ..., priority_boost: _Optional[int] = ..., stream_id: _Optional[str] = ..., max_weight: _Optional[float] = ..., min_weight: _Optional[float] = ...) -> None: ...

class StreamResult(_message.Message):
    __slots__ = ("stream_id", "allocated_weight")
    STREAM_ID_FIELD_NUMBER: _ClassVar[int]
    ALLOCATED_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    stream_id: str
    allocated_weight: float
    def __init__(self, stream_id: _Optional[str] = ..., allocated_weight: _Optional[float] = ...) -> None: ...
