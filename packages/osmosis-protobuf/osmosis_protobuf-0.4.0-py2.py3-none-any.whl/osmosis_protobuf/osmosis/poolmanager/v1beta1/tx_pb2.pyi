from gogoproto import gogo_pb2 as _gogo_pb2
from amino import amino_pb2 as _amino_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from osmosis.poolmanager.v1beta1 import swap_route_pb2 as _swap_route_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class MsgSwapExactAmountIn(_message.Message):
    __slots__ = ['sender', 'routes', 'token_in', 'token_out_min_amount']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    ROUTES_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IN_FIELD_NUMBER: _ClassVar[int]
    TOKEN_OUT_MIN_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    sender: str
    routes: _containers.RepeatedCompositeFieldContainer[_swap_route_pb2.SwapAmountInRoute]
    token_in: _coin_pb2.Coin
    token_out_min_amount: str

    def __init__(self, sender: _Optional[str]=..., routes: _Optional[_Iterable[_Union[_swap_route_pb2.SwapAmountInRoute, _Mapping]]]=..., token_in: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=..., token_out_min_amount: _Optional[str]=...) -> None:
        ...

class MsgSwapExactAmountInResponse(_message.Message):
    __slots__ = ['token_out_amount']
    TOKEN_OUT_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    token_out_amount: str

    def __init__(self, token_out_amount: _Optional[str]=...) -> None:
        ...

class MsgSplitRouteSwapExactAmountIn(_message.Message):
    __slots__ = ['sender', 'routes', 'token_in_denom', 'token_out_min_amount']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    ROUTES_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IN_DENOM_FIELD_NUMBER: _ClassVar[int]
    TOKEN_OUT_MIN_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    sender: str
    routes: _containers.RepeatedCompositeFieldContainer[_swap_route_pb2.SwapAmountInSplitRoute]
    token_in_denom: str
    token_out_min_amount: str

    def __init__(self, sender: _Optional[str]=..., routes: _Optional[_Iterable[_Union[_swap_route_pb2.SwapAmountInSplitRoute, _Mapping]]]=..., token_in_denom: _Optional[str]=..., token_out_min_amount: _Optional[str]=...) -> None:
        ...

class MsgSplitRouteSwapExactAmountInResponse(_message.Message):
    __slots__ = ['token_out_amount']
    TOKEN_OUT_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    token_out_amount: str

    def __init__(self, token_out_amount: _Optional[str]=...) -> None:
        ...

class MsgSwapExactAmountOut(_message.Message):
    __slots__ = ['sender', 'routes', 'token_in_max_amount', 'token_out']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    ROUTES_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IN_MAX_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    TOKEN_OUT_FIELD_NUMBER: _ClassVar[int]
    sender: str
    routes: _containers.RepeatedCompositeFieldContainer[_swap_route_pb2.SwapAmountOutRoute]
    token_in_max_amount: str
    token_out: _coin_pb2.Coin

    def __init__(self, sender: _Optional[str]=..., routes: _Optional[_Iterable[_Union[_swap_route_pb2.SwapAmountOutRoute, _Mapping]]]=..., token_in_max_amount: _Optional[str]=..., token_out: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=...) -> None:
        ...

class MsgSwapExactAmountOutResponse(_message.Message):
    __slots__ = ['token_in_amount']
    TOKEN_IN_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    token_in_amount: str

    def __init__(self, token_in_amount: _Optional[str]=...) -> None:
        ...

class MsgSplitRouteSwapExactAmountOut(_message.Message):
    __slots__ = ['sender', 'routes', 'token_out_denom', 'token_in_max_amount']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    ROUTES_FIELD_NUMBER: _ClassVar[int]
    TOKEN_OUT_DENOM_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IN_MAX_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    sender: str
    routes: _containers.RepeatedCompositeFieldContainer[_swap_route_pb2.SwapAmountOutSplitRoute]
    token_out_denom: str
    token_in_max_amount: str

    def __init__(self, sender: _Optional[str]=..., routes: _Optional[_Iterable[_Union[_swap_route_pb2.SwapAmountOutSplitRoute, _Mapping]]]=..., token_out_denom: _Optional[str]=..., token_in_max_amount: _Optional[str]=...) -> None:
        ...

class MsgSplitRouteSwapExactAmountOutResponse(_message.Message):
    __slots__ = ['token_in_amount']
    TOKEN_IN_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    token_in_amount: str

    def __init__(self, token_in_amount: _Optional[str]=...) -> None:
        ...

class MsgSetDenomPairTakerFee(_message.Message):
    __slots__ = ['sender', 'denom_pair_taker_fee']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    DENOM_PAIR_TAKER_FEE_FIELD_NUMBER: _ClassVar[int]
    sender: str
    denom_pair_taker_fee: _containers.RepeatedCompositeFieldContainer[DenomPairTakerFee]

    def __init__(self, sender: _Optional[str]=..., denom_pair_taker_fee: _Optional[_Iterable[_Union[DenomPairTakerFee, _Mapping]]]=...) -> None:
        ...

class MsgSetDenomPairTakerFeeResponse(_message.Message):
    __slots__ = ['success']
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool

    def __init__(self, success: bool=...) -> None:
        ...

class DenomPairTakerFee(_message.Message):
    __slots__ = ['denom0', 'denom1', 'taker_fee']
    DENOM0_FIELD_NUMBER: _ClassVar[int]
    DENOM1_FIELD_NUMBER: _ClassVar[int]
    TAKER_FEE_FIELD_NUMBER: _ClassVar[int]
    denom0: str
    denom1: str
    taker_fee: str

    def __init__(self, denom0: _Optional[str]=..., denom1: _Optional[str]=..., taker_fee: _Optional[str]=...) -> None:
        ...