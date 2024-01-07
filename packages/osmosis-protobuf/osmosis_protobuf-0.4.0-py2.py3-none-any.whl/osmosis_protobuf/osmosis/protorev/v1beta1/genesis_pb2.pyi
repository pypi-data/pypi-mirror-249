from gogoproto import gogo_pb2 as _gogo_pb2
from osmosis.protorev.v1beta1 import protorev_pb2 as _protorev_pb2
from osmosis.protorev.v1beta1 import params_pb2 as _params_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class GenesisState(_message.Message):
    __slots__ = ['params', 'token_pair_arb_routes', 'base_denoms', 'pool_weights', 'days_since_module_genesis', 'developer_fees', 'latest_block_height', 'developer_address', 'max_pool_points_per_block', 'max_pool_points_per_tx', 'point_count_for_block', 'profits', 'info_by_pool_type', 'cyclic_arb_tracker']
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    TOKEN_PAIR_ARB_ROUTES_FIELD_NUMBER: _ClassVar[int]
    BASE_DENOMS_FIELD_NUMBER: _ClassVar[int]
    POOL_WEIGHTS_FIELD_NUMBER: _ClassVar[int]
    DAYS_SINCE_MODULE_GENESIS_FIELD_NUMBER: _ClassVar[int]
    DEVELOPER_FEES_FIELD_NUMBER: _ClassVar[int]
    LATEST_BLOCK_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    DEVELOPER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    MAX_POOL_POINTS_PER_BLOCK_FIELD_NUMBER: _ClassVar[int]
    MAX_POOL_POINTS_PER_TX_FIELD_NUMBER: _ClassVar[int]
    POINT_COUNT_FOR_BLOCK_FIELD_NUMBER: _ClassVar[int]
    PROFITS_FIELD_NUMBER: _ClassVar[int]
    INFO_BY_POOL_TYPE_FIELD_NUMBER: _ClassVar[int]
    CYCLIC_ARB_TRACKER_FIELD_NUMBER: _ClassVar[int]
    params: _params_pb2.Params
    token_pair_arb_routes: _containers.RepeatedCompositeFieldContainer[_protorev_pb2.TokenPairArbRoutes]
    base_denoms: _containers.RepeatedCompositeFieldContainer[_protorev_pb2.BaseDenom]
    pool_weights: _protorev_pb2.PoolWeights
    days_since_module_genesis: int
    developer_fees: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    latest_block_height: int
    developer_address: str
    max_pool_points_per_block: int
    max_pool_points_per_tx: int
    point_count_for_block: int
    profits: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    info_by_pool_type: _protorev_pb2.InfoByPoolType
    cyclic_arb_tracker: _protorev_pb2.CyclicArbTracker

    def __init__(self, params: _Optional[_Union[_params_pb2.Params, _Mapping]]=..., token_pair_arb_routes: _Optional[_Iterable[_Union[_protorev_pb2.TokenPairArbRoutes, _Mapping]]]=..., base_denoms: _Optional[_Iterable[_Union[_protorev_pb2.BaseDenom, _Mapping]]]=..., pool_weights: _Optional[_Union[_protorev_pb2.PoolWeights, _Mapping]]=..., days_since_module_genesis: _Optional[int]=..., developer_fees: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=..., latest_block_height: _Optional[int]=..., developer_address: _Optional[str]=..., max_pool_points_per_block: _Optional[int]=..., max_pool_points_per_tx: _Optional[int]=..., point_count_for_block: _Optional[int]=..., profits: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=..., info_by_pool_type: _Optional[_Union[_protorev_pb2.InfoByPoolType, _Mapping]]=..., cyclic_arb_tracker: _Optional[_Union[_protorev_pb2.CyclicArbTracker, _Mapping]]=...) -> None:
        ...