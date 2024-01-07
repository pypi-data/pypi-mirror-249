from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class PoolType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    Balancer: _ClassVar[PoolType]
    Stableswap: _ClassVar[PoolType]
    Concentrated: _ClassVar[PoolType]
    CosmWasm: _ClassVar[PoolType]
Balancer: PoolType
Stableswap: PoolType
Concentrated: PoolType
CosmWasm: PoolType

class ModuleRoute(_message.Message):
    __slots__ = ['pool_type', 'pool_id']
    POOL_TYPE_FIELD_NUMBER: _ClassVar[int]
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    pool_type: PoolType
    pool_id: int

    def __init__(self, pool_type: _Optional[_Union[PoolType, str]]=..., pool_id: _Optional[int]=...) -> None:
        ...