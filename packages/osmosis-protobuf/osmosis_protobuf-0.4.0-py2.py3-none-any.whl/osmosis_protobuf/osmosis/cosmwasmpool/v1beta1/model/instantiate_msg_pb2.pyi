from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class InstantiateMsg(_message.Message):
    __slots__ = ['pool_asset_denoms']
    POOL_ASSET_DENOMS_FIELD_NUMBER: _ClassVar[int]
    pool_asset_denoms: _containers.RepeatedScalarFieldContainer[str]

    def __init__(self, pool_asset_denoms: _Optional[_Iterable[str]]=...) -> None:
        ...