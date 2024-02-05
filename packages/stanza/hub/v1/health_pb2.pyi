from google.api import annotations_pb2 as _annotations_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from stanza.hub.v1 import common_pb2 as _common_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QueryGuardHealthRequest(_message.Message):
    __slots__ = ("selector", "priority_boost")
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_BOOST_FIELD_NUMBER: _ClassVar[int]
    selector: _common_pb2.GuardFeatureSelector
    priority_boost: int
    def __init__(self, selector: _Optional[_Union[_common_pb2.GuardFeatureSelector, _Mapping]] = ..., priority_boost: _Optional[int] = ...) -> None: ...

class QueryGuardHealthResponse(_message.Message):
    __slots__ = ("health",)
    HEALTH_FIELD_NUMBER: _ClassVar[int]
    health: _common_pb2.Health
    def __init__(self, health: _Optional[_Union[_common_pb2.Health, str]] = ...) -> None: ...
