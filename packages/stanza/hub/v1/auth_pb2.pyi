from google.api import annotations_pb2 as _annotations_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetBearerTokenRequest(_message.Message):
    __slots__ = ("environment",)
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    environment: str
    def __init__(self, environment: _Optional[str] = ...) -> None: ...

class GetBearerTokenResponse(_message.Message):
    __slots__ = ("bearer_token",)
    BEARER_TOKEN_FIELD_NUMBER: _ClassVar[int]
    bearer_token: str
    def __init__(self, bearer_token: _Optional[str] = ...) -> None: ...
