from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class SwapAmountInRoute(_message.Message):
    __slots__ = ['pool_id', 'token_out_denom']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_OUT_DENOM_FIELD_NUMBER: _ClassVar[int]
    pool_id: int
    token_out_denom: str

    def __init__(self, pool_id: _Optional[int]=..., token_out_denom: _Optional[str]=...) -> None:
        ...

class SwapAmountOutRoute(_message.Message):
    __slots__ = ['pool_id', 'token_in_denom']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IN_DENOM_FIELD_NUMBER: _ClassVar[int]
    pool_id: int
    token_in_denom: str

    def __init__(self, pool_id: _Optional[int]=..., token_in_denom: _Optional[str]=...) -> None:
        ...

class SwapAmountInSplitRoute(_message.Message):
    __slots__ = ['pools', 'token_in_amount']
    POOLS_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IN_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    pools: _containers.RepeatedCompositeFieldContainer[SwapAmountInRoute]
    token_in_amount: str

    def __init__(self, pools: _Optional[_Iterable[_Union[SwapAmountInRoute, _Mapping]]]=..., token_in_amount: _Optional[str]=...) -> None:
        ...

class SwapAmountOutSplitRoute(_message.Message):
    __slots__ = ['pools', 'token_out_amount']
    POOLS_FIELD_NUMBER: _ClassVar[int]
    TOKEN_OUT_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    pools: _containers.RepeatedCompositeFieldContainer[SwapAmountOutRoute]
    token_out_amount: str

    def __init__(self, pools: _Optional[_Iterable[_Union[SwapAmountOutRoute, _Mapping]]]=..., token_out_amount: _Optional[str]=...) -> None:
        ...