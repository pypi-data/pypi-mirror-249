from gogoproto import gogo_pb2 as _gogo_pb2
from osmosis.poolmanager.v1beta1 import genesis_pb2 as _genesis_pb2
from osmosis.poolmanager.v1beta1 import tx_pb2 as _tx_pb2
from osmosis.poolmanager.v1beta1 import swap_route_pb2 as _swap_route_pb2
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
    params: _genesis_pb2.Params

    def __init__(self, params: _Optional[_Union[_genesis_pb2.Params, _Mapping]]=...) -> None:
        ...

class EstimateSwapExactAmountInRequest(_message.Message):
    __slots__ = ['pool_id', 'token_in', 'routes']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IN_FIELD_NUMBER: _ClassVar[int]
    ROUTES_FIELD_NUMBER: _ClassVar[int]
    pool_id: int
    token_in: str
    routes: _containers.RepeatedCompositeFieldContainer[_swap_route_pb2.SwapAmountInRoute]

    def __init__(self, pool_id: _Optional[int]=..., token_in: _Optional[str]=..., routes: _Optional[_Iterable[_Union[_swap_route_pb2.SwapAmountInRoute, _Mapping]]]=...) -> None:
        ...

class EstimateSwapExactAmountInWithPrimitiveTypesRequest(_message.Message):
    __slots__ = ['pool_id', 'token_in', 'routes_pool_id', 'routes_token_out_denom']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IN_FIELD_NUMBER: _ClassVar[int]
    ROUTES_POOL_ID_FIELD_NUMBER: _ClassVar[int]
    ROUTES_TOKEN_OUT_DENOM_FIELD_NUMBER: _ClassVar[int]
    pool_id: int
    token_in: str
    routes_pool_id: _containers.RepeatedScalarFieldContainer[int]
    routes_token_out_denom: _containers.RepeatedScalarFieldContainer[str]

    def __init__(self, pool_id: _Optional[int]=..., token_in: _Optional[str]=..., routes_pool_id: _Optional[_Iterable[int]]=..., routes_token_out_denom: _Optional[_Iterable[str]]=...) -> None:
        ...

class EstimateSinglePoolSwapExactAmountInRequest(_message.Message):
    __slots__ = ['pool_id', 'token_in', 'token_out_denom']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IN_FIELD_NUMBER: _ClassVar[int]
    TOKEN_OUT_DENOM_FIELD_NUMBER: _ClassVar[int]
    pool_id: int
    token_in: str
    token_out_denom: str

    def __init__(self, pool_id: _Optional[int]=..., token_in: _Optional[str]=..., token_out_denom: _Optional[str]=...) -> None:
        ...

class EstimateSwapExactAmountInResponse(_message.Message):
    __slots__ = ['token_out_amount']
    TOKEN_OUT_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    token_out_amount: str

    def __init__(self, token_out_amount: _Optional[str]=...) -> None:
        ...

class EstimateSwapExactAmountOutRequest(_message.Message):
    __slots__ = ['pool_id', 'routes', 'token_out']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    ROUTES_FIELD_NUMBER: _ClassVar[int]
    TOKEN_OUT_FIELD_NUMBER: _ClassVar[int]
    pool_id: int
    routes: _containers.RepeatedCompositeFieldContainer[_swap_route_pb2.SwapAmountOutRoute]
    token_out: str

    def __init__(self, pool_id: _Optional[int]=..., routes: _Optional[_Iterable[_Union[_swap_route_pb2.SwapAmountOutRoute, _Mapping]]]=..., token_out: _Optional[str]=...) -> None:
        ...

class EstimateSwapExactAmountOutWithPrimitiveTypesRequest(_message.Message):
    __slots__ = ['pool_id', 'routes_pool_id', 'routes_token_in_denom', 'token_out']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    ROUTES_POOL_ID_FIELD_NUMBER: _ClassVar[int]
    ROUTES_TOKEN_IN_DENOM_FIELD_NUMBER: _ClassVar[int]
    TOKEN_OUT_FIELD_NUMBER: _ClassVar[int]
    pool_id: int
    routes_pool_id: _containers.RepeatedScalarFieldContainer[int]
    routes_token_in_denom: _containers.RepeatedScalarFieldContainer[str]
    token_out: str

    def __init__(self, pool_id: _Optional[int]=..., routes_pool_id: _Optional[_Iterable[int]]=..., routes_token_in_denom: _Optional[_Iterable[str]]=..., token_out: _Optional[str]=...) -> None:
        ...

class EstimateSinglePoolSwapExactAmountOutRequest(_message.Message):
    __slots__ = ['pool_id', 'token_in_denom', 'token_out']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IN_DENOM_FIELD_NUMBER: _ClassVar[int]
    TOKEN_OUT_FIELD_NUMBER: _ClassVar[int]
    pool_id: int
    token_in_denom: str
    token_out: str

    def __init__(self, pool_id: _Optional[int]=..., token_in_denom: _Optional[str]=..., token_out: _Optional[str]=...) -> None:
        ...

class EstimateSwapExactAmountOutResponse(_message.Message):
    __slots__ = ['token_in_amount']
    TOKEN_IN_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    token_in_amount: str

    def __init__(self, token_in_amount: _Optional[str]=...) -> None:
        ...

class NumPoolsRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class NumPoolsResponse(_message.Message):
    __slots__ = ['num_pools']
    NUM_POOLS_FIELD_NUMBER: _ClassVar[int]
    num_pools: int

    def __init__(self, num_pools: _Optional[int]=...) -> None:
        ...

class PoolRequest(_message.Message):
    __slots__ = ['pool_id']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    pool_id: int

    def __init__(self, pool_id: _Optional[int]=...) -> None:
        ...

class PoolResponse(_message.Message):
    __slots__ = ['pool']
    POOL_FIELD_NUMBER: _ClassVar[int]
    pool: _any_pb2.Any

    def __init__(self, pool: _Optional[_Union[_any_pb2.Any, _Mapping]]=...) -> None:
        ...

class AllPoolsRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class AllPoolsResponse(_message.Message):
    __slots__ = ['pools']
    POOLS_FIELD_NUMBER: _ClassVar[int]
    pools: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]

    def __init__(self, pools: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]]=...) -> None:
        ...

class ListPoolsByDenomRequest(_message.Message):
    __slots__ = ['denom']
    DENOM_FIELD_NUMBER: _ClassVar[int]
    denom: str

    def __init__(self, denom: _Optional[str]=...) -> None:
        ...

class ListPoolsByDenomResponse(_message.Message):
    __slots__ = ['pools']
    POOLS_FIELD_NUMBER: _ClassVar[int]
    pools: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]

    def __init__(self, pools: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]]=...) -> None:
        ...

class SpotPriceRequest(_message.Message):
    __slots__ = ['pool_id', 'base_asset_denom', 'quote_asset_denom']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    BASE_ASSET_DENOM_FIELD_NUMBER: _ClassVar[int]
    QUOTE_ASSET_DENOM_FIELD_NUMBER: _ClassVar[int]
    pool_id: int
    base_asset_denom: str
    quote_asset_denom: str

    def __init__(self, pool_id: _Optional[int]=..., base_asset_denom: _Optional[str]=..., quote_asset_denom: _Optional[str]=...) -> None:
        ...

class SpotPriceResponse(_message.Message):
    __slots__ = ['spot_price']
    SPOT_PRICE_FIELD_NUMBER: _ClassVar[int]
    spot_price: str

    def __init__(self, spot_price: _Optional[str]=...) -> None:
        ...

class TotalPoolLiquidityRequest(_message.Message):
    __slots__ = ['pool_id']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    pool_id: int

    def __init__(self, pool_id: _Optional[int]=...) -> None:
        ...

class TotalPoolLiquidityResponse(_message.Message):
    __slots__ = ['liquidity']
    LIQUIDITY_FIELD_NUMBER: _ClassVar[int]
    liquidity: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, liquidity: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class TotalLiquidityRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class TotalLiquidityResponse(_message.Message):
    __slots__ = ['liquidity']
    LIQUIDITY_FIELD_NUMBER: _ClassVar[int]
    liquidity: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, liquidity: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class TotalVolumeForPoolRequest(_message.Message):
    __slots__ = ['pool_id']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    pool_id: int

    def __init__(self, pool_id: _Optional[int]=...) -> None:
        ...

class TotalVolumeForPoolResponse(_message.Message):
    __slots__ = ['volume']
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    volume: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, volume: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class TradingPairTakerFeeRequest(_message.Message):
    __slots__ = ['denom_0', 'denom_1']
    DENOM_0_FIELD_NUMBER: _ClassVar[int]
    DENOM_1_FIELD_NUMBER: _ClassVar[int]
    denom_0: str
    denom_1: str

    def __init__(self, denom_0: _Optional[str]=..., denom_1: _Optional[str]=...) -> None:
        ...

class TradingPairTakerFeeResponse(_message.Message):
    __slots__ = ['taker_fee']
    TAKER_FEE_FIELD_NUMBER: _ClassVar[int]
    taker_fee: str

    def __init__(self, taker_fee: _Optional[str]=...) -> None:
        ...

class EstimateTradeBasedOnPriceImpactRequest(_message.Message):
    __slots__ = ['from_coin', 'to_coin_denom', 'pool_id', 'max_price_impact', 'external_price']
    FROM_COIN_FIELD_NUMBER: _ClassVar[int]
    TO_COIN_DENOM_FIELD_NUMBER: _ClassVar[int]
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    MAX_PRICE_IMPACT_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_PRICE_FIELD_NUMBER: _ClassVar[int]
    from_coin: _coin_pb2.Coin
    to_coin_denom: str
    pool_id: int
    max_price_impact: str
    external_price: str

    def __init__(self, from_coin: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=..., to_coin_denom: _Optional[str]=..., pool_id: _Optional[int]=..., max_price_impact: _Optional[str]=..., external_price: _Optional[str]=...) -> None:
        ...

class EstimateTradeBasedOnPriceImpactResponse(_message.Message):
    __slots__ = ['input_coin', 'output_coin']
    INPUT_COIN_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_COIN_FIELD_NUMBER: _ClassVar[int]
    input_coin: _coin_pb2.Coin
    output_coin: _coin_pb2.Coin

    def __init__(self, input_coin: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=..., output_coin: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=...) -> None:
        ...