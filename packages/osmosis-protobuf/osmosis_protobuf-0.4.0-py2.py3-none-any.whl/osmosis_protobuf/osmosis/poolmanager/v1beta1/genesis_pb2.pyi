from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import any_pb2 as _any_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from osmosis.poolmanager.v1beta1 import module_route_pb2 as _module_route_pb2
from osmosis.poolmanager.v1beta1 import tx_pb2 as _tx_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class Params(_message.Message):
    __slots__ = ['pool_creation_fee', 'taker_fee_params', 'authorized_quote_denoms']
    POOL_CREATION_FEE_FIELD_NUMBER: _ClassVar[int]
    TAKER_FEE_PARAMS_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZED_QUOTE_DENOMS_FIELD_NUMBER: _ClassVar[int]
    pool_creation_fee: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    taker_fee_params: TakerFeeParams
    authorized_quote_denoms: _containers.RepeatedScalarFieldContainer[str]

    def __init__(self, pool_creation_fee: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=..., taker_fee_params: _Optional[_Union[TakerFeeParams, _Mapping]]=..., authorized_quote_denoms: _Optional[_Iterable[str]]=...) -> None:
        ...

class GenesisState(_message.Message):
    __slots__ = ['next_pool_id', 'params', 'pool_routes', 'taker_fees_tracker', 'pool_volumes', 'denom_pair_taker_fee_store']
    NEXT_POOL_ID_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    POOL_ROUTES_FIELD_NUMBER: _ClassVar[int]
    TAKER_FEES_TRACKER_FIELD_NUMBER: _ClassVar[int]
    POOL_VOLUMES_FIELD_NUMBER: _ClassVar[int]
    DENOM_PAIR_TAKER_FEE_STORE_FIELD_NUMBER: _ClassVar[int]
    next_pool_id: int
    params: Params
    pool_routes: _containers.RepeatedCompositeFieldContainer[_module_route_pb2.ModuleRoute]
    taker_fees_tracker: TakerFeesTracker
    pool_volumes: _containers.RepeatedCompositeFieldContainer[PoolVolume]
    denom_pair_taker_fee_store: _containers.RepeatedCompositeFieldContainer[_tx_pb2.DenomPairTakerFee]

    def __init__(self, next_pool_id: _Optional[int]=..., params: _Optional[_Union[Params, _Mapping]]=..., pool_routes: _Optional[_Iterable[_Union[_module_route_pb2.ModuleRoute, _Mapping]]]=..., taker_fees_tracker: _Optional[_Union[TakerFeesTracker, _Mapping]]=..., pool_volumes: _Optional[_Iterable[_Union[PoolVolume, _Mapping]]]=..., denom_pair_taker_fee_store: _Optional[_Iterable[_Union[_tx_pb2.DenomPairTakerFee, _Mapping]]]=...) -> None:
        ...

class TakerFeeParams(_message.Message):
    __slots__ = ['default_taker_fee', 'osmo_taker_fee_distribution', 'non_osmo_taker_fee_distribution', 'admin_addresses', 'community_pool_denom_to_swap_non_whitelisted_assets_to', 'reduced_fee_whitelist']
    DEFAULT_TAKER_FEE_FIELD_NUMBER: _ClassVar[int]
    OSMO_TAKER_FEE_DISTRIBUTION_FIELD_NUMBER: _ClassVar[int]
    NON_OSMO_TAKER_FEE_DISTRIBUTION_FIELD_NUMBER: _ClassVar[int]
    ADMIN_ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    COMMUNITY_POOL_DENOM_TO_SWAP_NON_WHITELISTED_ASSETS_TO_FIELD_NUMBER: _ClassVar[int]
    REDUCED_FEE_WHITELIST_FIELD_NUMBER: _ClassVar[int]
    default_taker_fee: str
    osmo_taker_fee_distribution: TakerFeeDistributionPercentage
    non_osmo_taker_fee_distribution: TakerFeeDistributionPercentage
    admin_addresses: _containers.RepeatedScalarFieldContainer[str]
    community_pool_denom_to_swap_non_whitelisted_assets_to: str
    reduced_fee_whitelist: _containers.RepeatedScalarFieldContainer[str]

    def __init__(self, default_taker_fee: _Optional[str]=..., osmo_taker_fee_distribution: _Optional[_Union[TakerFeeDistributionPercentage, _Mapping]]=..., non_osmo_taker_fee_distribution: _Optional[_Union[TakerFeeDistributionPercentage, _Mapping]]=..., admin_addresses: _Optional[_Iterable[str]]=..., community_pool_denom_to_swap_non_whitelisted_assets_to: _Optional[str]=..., reduced_fee_whitelist: _Optional[_Iterable[str]]=...) -> None:
        ...

class TakerFeeDistributionPercentage(_message.Message):
    __slots__ = ['staking_rewards', 'community_pool']
    STAKING_REWARDS_FIELD_NUMBER: _ClassVar[int]
    COMMUNITY_POOL_FIELD_NUMBER: _ClassVar[int]
    staking_rewards: str
    community_pool: str

    def __init__(self, staking_rewards: _Optional[str]=..., community_pool: _Optional[str]=...) -> None:
        ...

class TakerFeesTracker(_message.Message):
    __slots__ = ['taker_fees_to_stakers', 'taker_fees_to_community_pool', 'height_accounting_starts_from']
    TAKER_FEES_TO_STAKERS_FIELD_NUMBER: _ClassVar[int]
    TAKER_FEES_TO_COMMUNITY_POOL_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_ACCOUNTING_STARTS_FROM_FIELD_NUMBER: _ClassVar[int]
    taker_fees_to_stakers: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    taker_fees_to_community_pool: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    height_accounting_starts_from: int

    def __init__(self, taker_fees_to_stakers: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=..., taker_fees_to_community_pool: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=..., height_accounting_starts_from: _Optional[int]=...) -> None:
        ...

class PoolVolume(_message.Message):
    __slots__ = ['pool_id', 'pool_volume']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    POOL_VOLUME_FIELD_NUMBER: _ClassVar[int]
    pool_id: int
    pool_volume: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, pool_id: _Optional[int]=..., pool_volume: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...