from gogoproto import gogo_pb2 as _gogo_pb2
from osmosis.tokenfactory.v1beta1 import authorityMetadata_pb2 as _authorityMetadata_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class Params(_message.Message):
    __slots__ = ['denom_creation_fee', 'denom_creation_gas_consume']
    DENOM_CREATION_FEE_FIELD_NUMBER: _ClassVar[int]
    DENOM_CREATION_GAS_CONSUME_FIELD_NUMBER: _ClassVar[int]
    denom_creation_fee: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    denom_creation_gas_consume: int

    def __init__(self, denom_creation_fee: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=..., denom_creation_gas_consume: _Optional[int]=...) -> None:
        ...