from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class GetSwapFeeQueryMsg(_message.Message):
    __slots__ = ['get_swap_fee']
    GET_SWAP_FEE_FIELD_NUMBER: _ClassVar[int]
    get_swap_fee: EmptyStruct

    def __init__(self, get_swap_fee: _Optional[_Union[EmptyStruct, _Mapping]]=...) -> None:
        ...

class GetSwapFeeQueryMsgResponse(_message.Message):
    __slots__ = ['swap_fee']
    SWAP_FEE_FIELD_NUMBER: _ClassVar[int]
    swap_fee: str

    def __init__(self, swap_fee: _Optional[str]=...) -> None:
        ...

class SpotPrice(_message.Message):
    __slots__ = ['quote_asset_denom', 'base_asset_denom']
    QUOTE_ASSET_DENOM_FIELD_NUMBER: _ClassVar[int]
    BASE_ASSET_DENOM_FIELD_NUMBER: _ClassVar[int]
    quote_asset_denom: str
    base_asset_denom: str

    def __init__(self, quote_asset_denom: _Optional[str]=..., base_asset_denom: _Optional[str]=...) -> None:
        ...

class SpotPriceQueryMsg(_message.Message):
    __slots__ = ['spot_price']
    SPOT_PRICE_FIELD_NUMBER: _ClassVar[int]
    spot_price: SpotPrice

    def __init__(self, spot_price: _Optional[_Union[SpotPrice, _Mapping]]=...) -> None:
        ...

class SpotPriceQueryMsgResponse(_message.Message):
    __slots__ = ['spot_price']
    SPOT_PRICE_FIELD_NUMBER: _ClassVar[int]
    spot_price: str

    def __init__(self, spot_price: _Optional[str]=...) -> None:
        ...

class EmptyStruct(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class GetTotalPoolLiquidityQueryMsg(_message.Message):
    __slots__ = ['get_total_pool_liquidity']
    GET_TOTAL_POOL_LIQUIDITY_FIELD_NUMBER: _ClassVar[int]
    get_total_pool_liquidity: EmptyStruct

    def __init__(self, get_total_pool_liquidity: _Optional[_Union[EmptyStruct, _Mapping]]=...) -> None:
        ...

class GetTotalPoolLiquidityQueryMsgResponse(_message.Message):
    __slots__ = ['total_pool_liquidity']
    TOTAL_POOL_LIQUIDITY_FIELD_NUMBER: _ClassVar[int]
    total_pool_liquidity: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, total_pool_liquidity: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class GetTotalSharesQueryMsg(_message.Message):
    __slots__ = ['get_total_shares']
    GET_TOTAL_SHARES_FIELD_NUMBER: _ClassVar[int]
    get_total_shares: EmptyStruct

    def __init__(self, get_total_shares: _Optional[_Union[EmptyStruct, _Mapping]]=...) -> None:
        ...

class GetTotalSharesQueryMsgResponse(_message.Message):
    __slots__ = ['total_shares']
    TOTAL_SHARES_FIELD_NUMBER: _ClassVar[int]
    total_shares: str

    def __init__(self, total_shares: _Optional[str]=...) -> None:
        ...