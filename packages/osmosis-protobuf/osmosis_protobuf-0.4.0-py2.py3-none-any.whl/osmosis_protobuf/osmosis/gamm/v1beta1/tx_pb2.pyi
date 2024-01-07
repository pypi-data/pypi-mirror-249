from gogoproto import gogo_pb2 as _gogo_pb2
from amino import amino_pb2 as _amino_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from osmosis.poolmanager.v1beta1 import swap_route_pb2 as _swap_route_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class MsgJoinPool(_message.Message):
    __slots__ = ['sender', 'pool_id', 'share_out_amount', 'token_in_maxs']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    SHARE_OUT_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IN_MAXS_FIELD_NUMBER: _ClassVar[int]
    sender: str
    pool_id: int
    share_out_amount: str
    token_in_maxs: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, sender: _Optional[str]=..., pool_id: _Optional[int]=..., share_out_amount: _Optional[str]=..., token_in_maxs: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class MsgJoinPoolResponse(_message.Message):
    __slots__ = ['share_out_amount', 'token_in']
    SHARE_OUT_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IN_FIELD_NUMBER: _ClassVar[int]
    share_out_amount: str
    token_in: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, share_out_amount: _Optional[str]=..., token_in: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class MsgExitPool(_message.Message):
    __slots__ = ['sender', 'pool_id', 'share_in_amount', 'token_out_mins']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    SHARE_IN_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    TOKEN_OUT_MINS_FIELD_NUMBER: _ClassVar[int]
    sender: str
    pool_id: int
    share_in_amount: str
    token_out_mins: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, sender: _Optional[str]=..., pool_id: _Optional[int]=..., share_in_amount: _Optional[str]=..., token_out_mins: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class MsgExitPoolResponse(_message.Message):
    __slots__ = ['token_out']
    TOKEN_OUT_FIELD_NUMBER: _ClassVar[int]
    token_out: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, token_out: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

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

class MsgJoinSwapExternAmountIn(_message.Message):
    __slots__ = ['sender', 'pool_id', 'token_in', 'share_out_min_amount']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IN_FIELD_NUMBER: _ClassVar[int]
    SHARE_OUT_MIN_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    sender: str
    pool_id: int
    token_in: _coin_pb2.Coin
    share_out_min_amount: str

    def __init__(self, sender: _Optional[str]=..., pool_id: _Optional[int]=..., token_in: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=..., share_out_min_amount: _Optional[str]=...) -> None:
        ...

class MsgJoinSwapExternAmountInResponse(_message.Message):
    __slots__ = ['share_out_amount']
    SHARE_OUT_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    share_out_amount: str

    def __init__(self, share_out_amount: _Optional[str]=...) -> None:
        ...

class MsgJoinSwapShareAmountOut(_message.Message):
    __slots__ = ['sender', 'pool_id', 'token_in_denom', 'share_out_amount', 'token_in_max_amount']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IN_DENOM_FIELD_NUMBER: _ClassVar[int]
    SHARE_OUT_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IN_MAX_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    sender: str
    pool_id: int
    token_in_denom: str
    share_out_amount: str
    token_in_max_amount: str

    def __init__(self, sender: _Optional[str]=..., pool_id: _Optional[int]=..., token_in_denom: _Optional[str]=..., share_out_amount: _Optional[str]=..., token_in_max_amount: _Optional[str]=...) -> None:
        ...

class MsgJoinSwapShareAmountOutResponse(_message.Message):
    __slots__ = ['token_in_amount']
    TOKEN_IN_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    token_in_amount: str

    def __init__(self, token_in_amount: _Optional[str]=...) -> None:
        ...

class MsgExitSwapShareAmountIn(_message.Message):
    __slots__ = ['sender', 'pool_id', 'token_out_denom', 'share_in_amount', 'token_out_min_amount']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_OUT_DENOM_FIELD_NUMBER: _ClassVar[int]
    SHARE_IN_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    TOKEN_OUT_MIN_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    sender: str
    pool_id: int
    token_out_denom: str
    share_in_amount: str
    token_out_min_amount: str

    def __init__(self, sender: _Optional[str]=..., pool_id: _Optional[int]=..., token_out_denom: _Optional[str]=..., share_in_amount: _Optional[str]=..., token_out_min_amount: _Optional[str]=...) -> None:
        ...

class MsgExitSwapShareAmountInResponse(_message.Message):
    __slots__ = ['token_out_amount']
    TOKEN_OUT_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    token_out_amount: str

    def __init__(self, token_out_amount: _Optional[str]=...) -> None:
        ...

class MsgExitSwapExternAmountOut(_message.Message):
    __slots__ = ['sender', 'pool_id', 'token_out', 'share_in_max_amount']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_OUT_FIELD_NUMBER: _ClassVar[int]
    SHARE_IN_MAX_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    sender: str
    pool_id: int
    token_out: _coin_pb2.Coin
    share_in_max_amount: str

    def __init__(self, sender: _Optional[str]=..., pool_id: _Optional[int]=..., token_out: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=..., share_in_max_amount: _Optional[str]=...) -> None:
        ...

class MsgExitSwapExternAmountOutResponse(_message.Message):
    __slots__ = ['share_in_amount']
    SHARE_IN_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    share_in_amount: str

    def __init__(self, share_in_amount: _Optional[str]=...) -> None:
        ...