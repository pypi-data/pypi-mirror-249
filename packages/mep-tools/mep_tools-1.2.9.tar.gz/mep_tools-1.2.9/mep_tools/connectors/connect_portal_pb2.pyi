from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TypeEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    ATS: _ClassVar[TypeEnum]
    CHANNEL: _ClassVar[TypeEnum]
    INTEGRATION: _ClassVar[TypeEnum]

class Operation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    GET: _ClassVar[Operation]
    CREATE: _ClassVar[Operation]
    READ: _ClassVar[Operation]
    UPDATE: _ClassVar[Operation]
    DELETE: _ClassVar[Operation]
ATS: TypeEnum
CHANNEL: TypeEnum
INTEGRATION: TypeEnum
GET: Operation
CREATE: Operation
READ: Operation
UPDATE: Operation
DELETE: Operation

class PortalGetRequest(_message.Message):
    __slots__ = ["uuid"]
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    def __init__(self, uuid: _Optional[str] = ...) -> None: ...

class PortalReadRequest(_message.Message):
    __slots__ = ["company_uuid"]
    COMPANY_UUID_FIELD_NUMBER: _ClassVar[int]
    company_uuid: str
    def __init__(self, company_uuid: _Optional[str] = ...) -> None: ...

class PortalDeleteRequest(_message.Message):
    __slots__ = ["uuid"]
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    def __init__(self, uuid: _Optional[str] = ...) -> None: ...

class PortalCreateRequest(_message.Message):
    __slots__ = ["company_uuid", "name", "type", "className", "config"]
    COMPANY_UUID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CLASSNAME_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    company_uuid: str
    name: str
    type: TypeEnum
    className: str
    config: _any_pb2.Any
    def __init__(self, company_uuid: _Optional[str] = ..., name: _Optional[str] = ..., type: _Optional[_Union[TypeEnum, str]] = ..., className: _Optional[str] = ..., config: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class PortalUpdateRequest(_message.Message):
    __slots__ = ["uuid", "name", "config"]
    UUID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    name: str
    config: _any_pb2.Any
    def __init__(self, uuid: _Optional[str] = ..., name: _Optional[str] = ..., config: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class PortalResponse(_message.Message):
    __slots__ = ["operation", "success", "uuid", "name", "type", "key", "className", "config", "created_at", "updated_at"]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    CLASSNAME_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    operation: Operation
    success: bool
    uuid: str
    name: str
    type: TypeEnum
    key: str
    className: str
    config: _any_pb2.Any
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, operation: _Optional[_Union[Operation, str]] = ..., success: bool = ..., uuid: _Optional[str] = ..., name: _Optional[str] = ..., type: _Optional[_Union[TypeEnum, str]] = ..., key: _Optional[str] = ..., className: _Optional[str] = ..., config: _Optional[_Union[_any_pb2.Any, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class PortalsResponse(_message.Message):
    __slots__ = ["portals"]
    PORTALS_FIELD_NUMBER: _ClassVar[int]
    portals: _containers.RepeatedCompositeFieldContainer[PortalResponse]
    def __init__(self, portals: _Optional[_Iterable[_Union[PortalResponse, _Mapping]]] = ...) -> None: ...
