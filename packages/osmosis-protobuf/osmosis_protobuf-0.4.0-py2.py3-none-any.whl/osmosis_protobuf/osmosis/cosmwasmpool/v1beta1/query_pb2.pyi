from gogoproto import gogo_pb2 as _gogo_pb2
from osmosis.cosmwasmpool.v1beta1 import params_pb2 as _params_pb2
from osmosis.cosmwasmpool.v1beta1 import tx_pb2 as _tx_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import any_pb2 as _any_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class ParamsRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class ParamsResponse(_message.Message):
    __slots__ = ['params']
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: _params_pb2.Params

    def __init__(self, params: _Optional[_Union[_params_pb2.Params, _Mapping]]=...) -> None:
        ...

class PoolsRequest(_message.Message):
    __slots__ = ['pagination']
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageRequest

    def __init__(self, pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]]=...) -> None:
        ...

class PoolsResponse(_message.Message):
    __slots__ = ['pools', 'pagination']
    POOLS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pools: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
    pagination: _pagination_pb2.PageResponse

    def __init__(self, pools: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]]=..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]]=...) -> None:
        ...

class ContractInfoByPoolIdRequest(_message.Message):
    __slots__ = ['pool_id']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    pool_id: int

    def __init__(self, pool_id: _Optional[int]=...) -> None:
        ...

class ContractInfoByPoolIdResponse(_message.Message):
    __slots__ = ['contract_address', 'code_id']
    CONTRACT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    CODE_ID_FIELD_NUMBER: _ClassVar[int]
    contract_address: str
    code_id: int

    def __init__(self, contract_address: _Optional[str]=..., code_id: _Optional[int]=...) -> None:
        ...