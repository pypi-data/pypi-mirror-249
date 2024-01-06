from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OperationEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    GET: _ClassVar[OperationEnum]
    CREATE: _ClassVar[OperationEnum]
    READ: _ClassVar[OperationEnum]
    UPDATE: _ClassVar[OperationEnum]
    DELETE: _ClassVar[OperationEnum]
GET: OperationEnum
CREATE: OperationEnum
READ: OperationEnum
UPDATE: OperationEnum
DELETE: OperationEnum

class CompanyGetRequest(_message.Message):
    __slots__ = ["company_name"]
    COMPANY_NAME_FIELD_NUMBER: _ClassVar[int]
    company_name: str
    def __init__(self, company_name: _Optional[str] = ...) -> None: ...

class CompanyCreateRequest(_message.Message):
    __slots__ = ["platform_uuid", "name", "configuration"]
    PLATFORM_UUID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    platform_uuid: _containers.RepeatedScalarFieldContainer[str]
    name: str
    configuration: _any_pb2.Any
    def __init__(self, platform_uuid: _Optional[_Iterable[str]] = ..., name: _Optional[str] = ..., configuration: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class CompanyUpdateRequest(_message.Message):
    __slots__ = ["uuid", "platform_uuid", "name", "configuration"]
    UUID_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_UUID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    platform_uuid: _containers.RepeatedScalarFieldContainer[str]
    name: str
    configuration: _any_pb2.Any
    def __init__(self, uuid: _Optional[str] = ..., platform_uuid: _Optional[_Iterable[str]] = ..., name: _Optional[str] = ..., configuration: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class CompanyResponse(_message.Message):
    __slots__ = ["operation", "uuid", "platform_uuid", "key", "name", "configuration", "created_at", "updated_at"]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_UUID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    operation: OperationEnum
    uuid: str
    platform_uuid: _containers.RepeatedScalarFieldContainer[str]
    key: str
    name: str
    configuration: _any_pb2.Any
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, operation: _Optional[_Union[OperationEnum, str]] = ..., uuid: _Optional[str] = ..., platform_uuid: _Optional[_Iterable[str]] = ..., key: _Optional[str] = ..., name: _Optional[str] = ..., configuration: _Optional[_Union[_any_pb2.Any, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
