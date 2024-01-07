from gogoproto import gogo_pb2 as _gogo_pb2
from osmosis.gamm.v1beta1 import tx_pb2 as _tx_pb2
from osmosis.poolmanager.v1beta1 import swap_route_pb2 as _swap_route_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import any_pb2 as _any_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from osmosis.gamm.v1beta1 import shared_pb2 as _shared_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class QueryPoolRequest(_message.Message):
    __slots__ = ['pool_id']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    pool_id: int

    def __init__(self, pool_id: _Optional[int]=...) -> None:
        ...

class QueryPoolResponse(_message.Message):
    __slots__ = ['pool']
    POOL_FIELD_NUMBER: _ClassVar[int]
    pool: _any_pb2.Any

    def __init__(self, pool: _Optional[_Union[_any_pb2.Any, _Mapping]]=...) -> None:
        ...

class QueryPoolsRequest(_message.Message):
    __slots__ = ['pagination']
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageRequest

    def __init__(self, pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]]=...) -> None:
        ...

class QueryPoolsResponse(_message.Message):
    __slots__ = ['pools', 'pagination']
    POOLS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pools: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
    pagination: _pagination_pb2.PageResponse

    def __init__(self, pools: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]]=..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]]=...) -> None:
        ...

class QueryNumPoolsRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryNumPoolsResponse(_message.Message):
    __slots__ = ['num_pools']
    NUM_POOLS_FIELD_NUMBER: _ClassVar[int]
    num_pools: int

    def __init__(self, num_pools: _Optional[int]=...) -> None:
        ...

class QueryPoolTypeRequest(_message.Message):
    __slots__ = ['pool_id']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    pool_id: int

    def __init__(self, pool_id: _Optional[int]=...) -> None:
        ...

class QueryPoolTypeResponse(_message.Message):
    __slots__ = ['pool_type']
    POOL_TYPE_FIELD_NUMBER: _ClassVar[int]
    pool_type: str

    def __init__(self, pool_type: _Optional[str]=...) -> None:
        ...

class QueryCalcJoinPoolSharesRequest(_message.Message):
    __slots__ = ['pool_id', 'tokens_in']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    TOKENS_IN_FIELD_NUMBER: _ClassVar[int]
    pool_id: int
    tokens_in: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, pool_id: _Optional[int]=..., tokens_in: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class QueryCalcJoinPoolSharesResponse(_message.Message):
    __slots__ = ['share_out_amount', 'tokens_out']
    SHARE_OUT_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    TOKENS_OUT_FIELD_NUMBER: _ClassVar[int]
    share_out_amount: str
    tokens_out: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, share_out_amount: _Optional[str]=..., tokens_out: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class QueryCalcExitPoolCoinsFromSharesRequest(_message.Message):
    __slots__ = ['pool_id', 'share_in_amount']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    SHARE_IN_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    pool_id: int
    share_in_amount: str

    def __init__(self, pool_id: _Optional[int]=..., share_in_amount: _Optional[str]=...) -> None:
        ...

class QueryCalcExitPoolCoinsFromSharesResponse(_message.Message):
    __slots__ = ['tokens_out']
    TOKENS_OUT_FIELD_NUMBER: _ClassVar[int]
    tokens_out: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, tokens_out: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class QueryPoolParamsRequest(_message.Message):
    __slots__ = ['pool_id']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    pool_id: int

    def __init__(self, pool_id: _Optional[int]=...) -> None:
        ...

class QueryPoolParamsResponse(_message.Message):
    __slots__ = ['params']
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: _any_pb2.Any

    def __init__(self, params: _Optional[_Union[_any_pb2.Any, _Mapping]]=...) -> None:
        ...

class QueryTotalPoolLiquidityRequest(_message.Message):
    __slots__ = ['pool_id']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    pool_id: int

    def __init__(self, pool_id: _Optional[int]=...) -> None:
        ...

class QueryTotalPoolLiquidityResponse(_message.Message):
    __slots__ = ['liquidity']
    LIQUIDITY_FIELD_NUMBER: _ClassVar[int]
    liquidity: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, liquidity: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class QueryTotalSharesRequest(_message.Message):
    __slots__ = ['pool_id']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    pool_id: int

    def __init__(self, pool_id: _Optional[int]=...) -> None:
        ...

class QueryTotalSharesResponse(_message.Message):
    __slots__ = ['total_shares']
    TOTAL_SHARES_FIELD_NUMBER: _ClassVar[int]
    total_shares: _coin_pb2.Coin

    def __init__(self, total_shares: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=...) -> None:
        ...

class QueryCalcJoinPoolNoSwapSharesRequest(_message.Message):
    __slots__ = ['pool_id', 'tokens_in']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    TOKENS_IN_FIELD_NUMBER: _ClassVar[int]
    pool_id: int
    tokens_in: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, pool_id: _Optional[int]=..., tokens_in: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class QueryCalcJoinPoolNoSwapSharesResponse(_message.Message):
    __slots__ = ['tokens_out', 'shares_out']
    TOKENS_OUT_FIELD_NUMBER: _ClassVar[int]
    SHARES_OUT_FIELD_NUMBER: _ClassVar[int]
    tokens_out: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    shares_out: str

    def __init__(self, tokens_out: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=..., shares_out: _Optional[str]=...) -> None:
        ...

class QuerySpotPriceRequest(_message.Message):
    __slots__ = ['pool_id', 'base_asset_denom', 'quote_asset_denom']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    BASE_ASSET_DENOM_FIELD_NUMBER: _ClassVar[int]
    QUOTE_ASSET_DENOM_FIELD_NUMBER: _ClassVar[int]
    pool_id: int
    base_asset_denom: str
    quote_asset_denom: str

    def __init__(self, pool_id: _Optional[int]=..., base_asset_denom: _Optional[str]=..., quote_asset_denom: _Optional[str]=...) -> None:
        ...

class QueryPoolsWithFilterRequest(_message.Message):
    __slots__ = ['min_liquidity', 'pool_type', 'pagination']
    MIN_LIQUIDITY_FIELD_NUMBER: _ClassVar[int]
    POOL_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    min_liquidity: str
    pool_type: str
    pagination: _pagination_pb2.PageRequest

    def __init__(self, min_liquidity: _Optional[str]=..., pool_type: _Optional[str]=..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]]=...) -> None:
        ...

class QueryPoolsWithFilterResponse(_message.Message):
    __slots__ = ['pools', 'pagination']
    POOLS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pools: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
    pagination: _pagination_pb2.PageResponse

    def __init__(self, pools: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]]=..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]]=...) -> None:
        ...

class QuerySpotPriceResponse(_message.Message):
    __slots__ = ['spot_price']
    SPOT_PRICE_FIELD_NUMBER: _ClassVar[int]
    spot_price: str

    def __init__(self, spot_price: _Optional[str]=...) -> None:
        ...

class QuerySwapExactAmountInRequest(_message.Message):
    __slots__ = ['sender', 'pool_id', 'token_in', 'routes']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IN_FIELD_NUMBER: _ClassVar[int]
    ROUTES_FIELD_NUMBER: _ClassVar[int]
    sender: str
    pool_id: int
    token_in: str
    routes: _containers.RepeatedCompositeFieldContainer[_swap_route_pb2.SwapAmountInRoute]

    def __init__(self, sender: _Optional[str]=..., pool_id: _Optional[int]=..., token_in: _Optional[str]=..., routes: _Optional[_Iterable[_Union[_swap_route_pb2.SwapAmountInRoute, _Mapping]]]=...) -> None:
        ...

class QuerySwapExactAmountInResponse(_message.Message):
    __slots__ = ['token_out_amount']
    TOKEN_OUT_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    token_out_amount: str

    def __init__(self, token_out_amount: _Optional[str]=...) -> None:
        ...

class QuerySwapExactAmountOutRequest(_message.Message):
    __slots__ = ['sender', 'pool_id', 'routes', 'token_out']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    ROUTES_FIELD_NUMBER: _ClassVar[int]
    TOKEN_OUT_FIELD_NUMBER: _ClassVar[int]
    sender: str
    pool_id: int
    routes: _containers.RepeatedCompositeFieldContainer[_swap_route_pb2.SwapAmountOutRoute]
    token_out: str

    def __init__(self, sender: _Optional[str]=..., pool_id: _Optional[int]=..., routes: _Optional[_Iterable[_Union[_swap_route_pb2.SwapAmountOutRoute, _Mapping]]]=..., token_out: _Optional[str]=...) -> None:
        ...

class QuerySwapExactAmountOutResponse(_message.Message):
    __slots__ = ['token_in_amount']
    TOKEN_IN_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    token_in_amount: str

    def __init__(self, token_in_amount: _Optional[str]=...) -> None:
        ...

class QueryTotalLiquidityRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryTotalLiquidityResponse(_message.Message):
    __slots__ = ['liquidity']
    LIQUIDITY_FIELD_NUMBER: _ClassVar[int]
    liquidity: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, liquidity: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class QueryConcentratedPoolIdLinkFromCFMMRequest(_message.Message):
    __slots__ = ['cfmm_pool_id']
    CFMM_POOL_ID_FIELD_NUMBER: _ClassVar[int]
    cfmm_pool_id: int

    def __init__(self, cfmm_pool_id: _Optional[int]=...) -> None:
        ...

class QueryConcentratedPoolIdLinkFromCFMMResponse(_message.Message):
    __slots__ = ['concentrated_pool_id']
    CONCENTRATED_POOL_ID_FIELD_NUMBER: _ClassVar[int]
    concentrated_pool_id: int

    def __init__(self, concentrated_pool_id: _Optional[int]=...) -> None:
        ...

class QueryCFMMConcentratedPoolLinksRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryCFMMConcentratedPoolLinksResponse(_message.Message):
    __slots__ = ['migration_records']
    MIGRATION_RECORDS_FIELD_NUMBER: _ClassVar[int]
    migration_records: _shared_pb2.MigrationRecords

    def __init__(self, migration_records: _Optional[_Union[_shared_pb2.MigrationRecords, _Mapping]]=...) -> None:
        ...