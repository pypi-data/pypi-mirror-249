from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import any_pb2 as _any_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from osmosis.cosmwasmpool.v1beta1 import params_pb2 as _params_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class GenesisState(_message.Message):
    __slots__ = ['params', 'pools']
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    POOLS_FIELD_NUMBER: _ClassVar[int]
    params: _params_pb2.Params
    pools: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]

    def __init__(self, params: _Optional[_Union[_params_pb2.Params, _Mapping]]=..., pools: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]]=...) -> None:
        ...