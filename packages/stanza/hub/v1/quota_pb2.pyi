from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from stanza.hub.v1 import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Reason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REASON_UNSPECIFIED: _ClassVar[Reason]
    REASON_SUFFICIENT_QUOTA: _ClassVar[Reason]
    REASON_INSUFFICIENT_QUOTA: _ClassVar[Reason]
    REASON_INSUFFICIENT_QUOTA_PARENT: _ClassVar[Reason]
    REASON_BURST: _ClassVar[Reason]
    REASON_BEST_EFFORT: _ClassVar[Reason]
REASON_UNSPECIFIED: Reason
REASON_SUFFICIENT_QUOTA: Reason
REASON_INSUFFICIENT_QUOTA: Reason
REASON_INSUFFICIENT_QUOTA_PARENT: Reason
REASON_BURST: Reason
REASON_BEST_EFFORT: Reason

class GetTokenRequest(_message.Message):
    __slots__ = ("selector", "client_id", "priority_boost", "weight")
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_BOOST_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    selector: _common_pb2.GuardFeatureSelector
    client_id: str
    priority_boost: int
    weight: float
    def __init__(self, selector: _Optional[_Union[_common_pb2.GuardFeatureSelector, _Mapping]] = ..., client_id: _Optional[str] = ..., priority_boost: _Optional[int] = ..., weight: _Optional[float] = ...) -> None: ...

class GetTokenResponse(_message.Message):
    __slots__ = ("granted", "token", "reason", "mode")
    GRANTED_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    granted: bool
    token: str
    reason: Reason
    mode: _common_pb2.Mode
    def __init__(self, granted: bool = ..., token: _Optional[str] = ..., reason: _Optional[_Union[Reason, str]] = ..., mode: _Optional[_Union[_common_pb2.Mode, str]] = ...) -> None: ...

class GetTokenLeaseRequest(_message.Message):
    __slots__ = ("selector", "client_id", "priority_boost", "default_weight")
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_BOOST_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    selector: _common_pb2.GuardFeatureSelector
    client_id: str
    priority_boost: int
    default_weight: float
    def __init__(self, selector: _Optional[_Union[_common_pb2.GuardFeatureSelector, _Mapping]] = ..., client_id: _Optional[str] = ..., priority_boost: _Optional[int] = ..., default_weight: _Optional[float] = ...) -> None: ...

class GetTokenLeaseResponse(_message.Message):
    __slots__ = ("granted", "leases")
    GRANTED_FIELD_NUMBER: _ClassVar[int]
    LEASES_FIELD_NUMBER: _ClassVar[int]
    granted: bool
    leases: _containers.RepeatedCompositeFieldContainer[TokenLease]
    def __init__(self, granted: bool = ..., leases: _Optional[_Iterable[_Union[TokenLease, _Mapping]]] = ...) -> None: ...

class TokenLease(_message.Message):
    __slots__ = ("duration_msec", "token", "feature", "priority_boost", "weight", "reason", "expires_at", "mode")
    DURATION_MSEC_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_BOOST_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    duration_msec: int
    token: str
    feature: str
    priority_boost: int
    weight: float
    reason: Reason
    expires_at: _timestamp_pb2.Timestamp
    mode: _common_pb2.Mode
    def __init__(self, duration_msec: _Optional[int] = ..., token: _Optional[str] = ..., feature: _Optional[str] = ..., priority_boost: _Optional[int] = ..., weight: _Optional[float] = ..., reason: _Optional[_Union[Reason, str]] = ..., expires_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., mode: _Optional[_Union[_common_pb2.Mode, str]] = ...) -> None: ...

class SetTokenLeaseConsumedRequest(_message.Message):
    __slots__ = ("tokens", "weight_correction", "environment")
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_CORRECTION_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    tokens: _containers.RepeatedScalarFieldContainer[str]
    weight_correction: float
    environment: str
    def __init__(self, tokens: _Optional[_Iterable[str]] = ..., weight_correction: _Optional[float] = ..., environment: _Optional[str] = ...) -> None: ...

class SetTokenLeaseConsumedResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ValidateTokenRequest(_message.Message):
    __slots__ = ("tokens",)
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    tokens: _containers.RepeatedCompositeFieldContainer[TokenInfo]
    def __init__(self, tokens: _Optional[_Iterable[_Union[TokenInfo, _Mapping]]] = ...) -> None: ...

class TokenInfo(_message.Message):
    __slots__ = ("token", "guard")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    GUARD_FIELD_NUMBER: _ClassVar[int]
    token: str
    guard: _common_pb2.GuardSelector
    def __init__(self, token: _Optional[str] = ..., guard: _Optional[_Union[_common_pb2.GuardSelector, _Mapping]] = ...) -> None: ...

class ValidateTokenResponse(_message.Message):
    __slots__ = ("valid", "tokens_valid")
    VALID_FIELD_NUMBER: _ClassVar[int]
    TOKENS_VALID_FIELD_NUMBER: _ClassVar[int]
    valid: bool
    tokens_valid: _containers.RepeatedCompositeFieldContainer[TokenValid]
    def __init__(self, valid: bool = ..., tokens_valid: _Optional[_Iterable[_Union[TokenValid, _Mapping]]] = ...) -> None: ...

class TokenValid(_message.Message):
    __slots__ = ("token", "valid")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    VALID_FIELD_NUMBER: _ClassVar[int]
    token: str
    valid: bool
    def __init__(self, token: _Optional[str] = ..., valid: bool = ...) -> None: ...
