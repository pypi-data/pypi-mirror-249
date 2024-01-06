from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

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
