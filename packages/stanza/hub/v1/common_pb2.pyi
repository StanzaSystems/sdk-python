from google.api import field_behavior_pb2 as _field_behavior_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Health(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HEALTH_UNSPECIFIED: _ClassVar[Health]
    HEALTH_OK: _ClassVar[Health]
    HEALTH_OVERLOAD: _ClassVar[Health]
    HEALTH_DOWN: _ClassVar[Health]

class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STATE_UNSPECIFIED: _ClassVar[State]
    STATE_ENABLED: _ClassVar[State]
    STATE_DISABLED: _ClassVar[State]

class Config(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONFIG_UNSPECIFIED: _ClassVar[Config]
    CONFIG_CACHED_OK: _ClassVar[Config]
    CONFIG_FETCHED_OK: _ClassVar[Config]
    CONFIG_NOT_FOUND: _ClassVar[Config]
    CONFIG_FETCH_ERROR: _ClassVar[Config]
    CONFIG_FETCH_TIMEOUT: _ClassVar[Config]

class Local(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOCAL_UNSPECIFIED: _ClassVar[Local]
    LOCAL_NOT_SUPPORTED: _ClassVar[Local]
    LOCAL_NOT_EVAL: _ClassVar[Local]
    LOCAL_EVAL_DISABLED: _ClassVar[Local]
    LOCAL_ALLOWED: _ClassVar[Local]
    LOCAL_BLOCKED: _ClassVar[Local]
    LOCAL_ERROR: _ClassVar[Local]

class Token(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TOKEN_UNSPECIFIED: _ClassVar[Token]
    TOKEN_NOT_EVAL: _ClassVar[Token]
    TOKEN_EVAL_DISABLED: _ClassVar[Token]
    TOKEN_NOT_VALID: _ClassVar[Token]
    TOKEN_VALID: _ClassVar[Token]
    TOKEN_VALIDATION_ERROR: _ClassVar[Token]
    TOKEN_VALIDATION_TIMEOUT: _ClassVar[Token]

class Quota(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    QUOTA_UNSPECIFIED: _ClassVar[Quota]
    QUOTA_NOT_EVAL: _ClassVar[Quota]
    QUOTA_EVAL_DISABLED: _ClassVar[Quota]
    QUOTA_LOCAL_ERROR: _ClassVar[Quota]
    QUOTA_BLOCKED: _ClassVar[Quota]
    QUOTA_GRANTED: _ClassVar[Quota]
    QUOTA_ERROR: _ClassVar[Quota]
    QUOTA_TIMEOUT: _ClassVar[Quota]

class Mode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MODE_UNSPECIFIED: _ClassVar[Mode]
    MODE_NORMAL: _ClassVar[Mode]
    MODE_REPORT_ONLY: _ClassVar[Mode]
HEALTH_UNSPECIFIED: Health
HEALTH_OK: Health
HEALTH_OVERLOAD: Health
HEALTH_DOWN: Health
STATE_UNSPECIFIED: State
STATE_ENABLED: State
STATE_DISABLED: State
CONFIG_UNSPECIFIED: Config
CONFIG_CACHED_OK: Config
CONFIG_FETCHED_OK: Config
CONFIG_NOT_FOUND: Config
CONFIG_FETCH_ERROR: Config
CONFIG_FETCH_TIMEOUT: Config
LOCAL_UNSPECIFIED: Local
LOCAL_NOT_SUPPORTED: Local
LOCAL_NOT_EVAL: Local
LOCAL_EVAL_DISABLED: Local
LOCAL_ALLOWED: Local
LOCAL_BLOCKED: Local
LOCAL_ERROR: Local
TOKEN_UNSPECIFIED: Token
TOKEN_NOT_EVAL: Token
TOKEN_EVAL_DISABLED: Token
TOKEN_NOT_VALID: Token
TOKEN_VALID: Token
TOKEN_VALIDATION_ERROR: Token
TOKEN_VALIDATION_TIMEOUT: Token
QUOTA_UNSPECIFIED: Quota
QUOTA_NOT_EVAL: Quota
QUOTA_EVAL_DISABLED: Quota
QUOTA_LOCAL_ERROR: Quota
QUOTA_BLOCKED: Quota
QUOTA_GRANTED: Quota
QUOTA_ERROR: Quota
QUOTA_TIMEOUT: Quota
MODE_UNSPECIFIED: Mode
MODE_NORMAL: Mode
MODE_REPORT_ONLY: Mode

class GuardSelector(_message.Message):
    __slots__ = ("environment", "name", "tags")
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    environment: str
    name: str
    tags: _containers.RepeatedCompositeFieldContainer[Tag]
    def __init__(self, environment: _Optional[str] = ..., name: _Optional[str] = ..., tags: _Optional[_Iterable[_Union[Tag, _Mapping]]] = ...) -> None: ...

class FeatureSelector(_message.Message):
    __slots__ = ("environment", "names", "tags")
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    NAMES_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    environment: str
    names: _containers.RepeatedScalarFieldContainer[str]
    tags: _containers.RepeatedCompositeFieldContainer[Tag]
    def __init__(self, environment: _Optional[str] = ..., names: _Optional[_Iterable[str]] = ..., tags: _Optional[_Iterable[_Union[Tag, _Mapping]]] = ...) -> None: ...

class GuardFeatureSelector(_message.Message):
    __slots__ = ("environment", "guard_name", "feature_name", "tags")
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    GUARD_NAME_FIELD_NUMBER: _ClassVar[int]
    FEATURE_NAME_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    environment: str
    guard_name: str
    feature_name: str
    tags: _containers.RepeatedCompositeFieldContainer[Tag]
    def __init__(self, environment: _Optional[str] = ..., guard_name: _Optional[str] = ..., feature_name: _Optional[str] = ..., tags: _Optional[_Iterable[_Union[Tag, _Mapping]]] = ...) -> None: ...

class GuardServiceSelector(_message.Message):
    __slots__ = ("environment", "guard_name", "service_name", "service_release", "tags")
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    GUARD_NAME_FIELD_NUMBER: _ClassVar[int]
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    SERVICE_RELEASE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    environment: str
    guard_name: str
    service_name: str
    service_release: str
    tags: _containers.RepeatedCompositeFieldContainer[Tag]
    def __init__(self, environment: _Optional[str] = ..., guard_name: _Optional[str] = ..., service_name: _Optional[str] = ..., service_release: _Optional[str] = ..., tags: _Optional[_Iterable[_Union[Tag, _Mapping]]] = ...) -> None: ...

class ServiceSelector(_message.Message):
    __slots__ = ("environment", "name", "release", "tags")
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    environment: str
    name: str
    release: str
    tags: _containers.RepeatedCompositeFieldContainer[Tag]
    def __init__(self, environment: _Optional[str] = ..., name: _Optional[str] = ..., release: _Optional[str] = ..., tags: _Optional[_Iterable[_Union[Tag, _Mapping]]] = ...) -> None: ...

class HealthByPriority(_message.Message):
    __slots__ = ("priority", "health")
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    HEALTH_FIELD_NUMBER: _ClassVar[int]
    priority: int
    health: Health
    def __init__(self, priority: _Optional[int] = ..., health: _Optional[_Union[Health, str]] = ...) -> None: ...

class Tag(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
