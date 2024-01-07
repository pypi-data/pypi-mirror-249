from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from osmosis.poolmanager.v1beta1 import genesis_pb2 as _genesis_pb2
from osmosis.txfees.v1beta1 import genesis_pb2 as _genesis_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class TokenPairArbRoutes(_message.Message):
    __slots__ = ['arb_routes', 'token_in', 'token_out']
    ARB_ROUTES_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IN_FIELD_NUMBER: _ClassVar[int]
    TOKEN_OUT_FIELD_NUMBER: _ClassVar[int]
    arb_routes: _containers.RepeatedCompositeFieldContainer[Route]
    token_in: str
    token_out: str

    def __init__(self, arb_routes: _Optional[_Iterable[_Union[Route, _Mapping]]]=..., token_in: _Optional[str]=..., token_out: _Optional[str]=...) -> None:
        ...

class Route(_message.Message):
    __slots__ = ['trades', 'step_size']
    TRADES_FIELD_NUMBER: _ClassVar[int]
    STEP_SIZE_FIELD_NUMBER: _ClassVar[int]
    trades: _containers.RepeatedCompositeFieldContainer[Trade]
    step_size: str

    def __init__(self, trades: _Optional[_Iterable[_Union[Trade, _Mapping]]]=..., step_size: _Optional[str]=...) -> None:
        ...

class Trade(_message.Message):
    __slots__ = ['pool', 'token_in', 'token_out']
    POOL_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IN_FIELD_NUMBER: _ClassVar[int]
    TOKEN_OUT_FIELD_NUMBER: _ClassVar[int]
    pool: int
    token_in: str
    token_out: str

    def __init__(self, pool: _Optional[int]=..., token_in: _Optional[str]=..., token_out: _Optional[str]=...) -> None:
        ...

class RouteStatistics(_message.Message):
    __slots__ = ['profits', 'number_of_trades', 'route']
    PROFITS_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_TRADES_FIELD_NUMBER: _ClassVar[int]
    ROUTE_FIELD_NUMBER: _ClassVar[int]
    profits: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    number_of_trades: str
    route: _containers.RepeatedScalarFieldContainer[int]

    def __init__(self, profits: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=..., number_of_trades: _Optional[str]=..., route: _Optional[_Iterable[int]]=...) -> None:
        ...

class PoolWeights(_message.Message):
    __slots__ = ['stable_weight', 'balancer_weight', 'concentrated_weight', 'cosmwasm_weight']
    STABLE_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    BALANCER_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    CONCENTRATED_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    COSMWASM_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    stable_weight: int
    balancer_weight: int
    concentrated_weight: int
    cosmwasm_weight: int

    def __init__(self, stable_weight: _Optional[int]=..., balancer_weight: _Optional[int]=..., concentrated_weight: _Optional[int]=..., cosmwasm_weight: _Optional[int]=...) -> None:
        ...

class InfoByPoolType(_message.Message):
    __slots__ = ['stable', 'balancer', 'concentrated', 'cosmwasm']
    STABLE_FIELD_NUMBER: _ClassVar[int]
    BALANCER_FIELD_NUMBER: _ClassVar[int]
    CONCENTRATED_FIELD_NUMBER: _ClassVar[int]
    COSMWASM_FIELD_NUMBER: _ClassVar[int]
    stable: StablePoolInfo
    balancer: BalancerPoolInfo
    concentrated: ConcentratedPoolInfo
    cosmwasm: CosmwasmPoolInfo

    def __init__(self, stable: _Optional[_Union[StablePoolInfo, _Mapping]]=..., balancer: _Optional[_Union[BalancerPoolInfo, _Mapping]]=..., concentrated: _Optional[_Union[ConcentratedPoolInfo, _Mapping]]=..., cosmwasm: _Optional[_Union[CosmwasmPoolInfo, _Mapping]]=...) -> None:
        ...

class StablePoolInfo(_message.Message):
    __slots__ = ['weight']
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    weight: int

    def __init__(self, weight: _Optional[int]=...) -> None:
        ...

class BalancerPoolInfo(_message.Message):
    __slots__ = ['weight']
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    weight: int

    def __init__(self, weight: _Optional[int]=...) -> None:
        ...

class ConcentratedPoolInfo(_message.Message):
    __slots__ = ['weight', 'max_ticks_crossed']
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    MAX_TICKS_CROSSED_FIELD_NUMBER: _ClassVar[int]
    weight: int
    max_ticks_crossed: int

    def __init__(self, weight: _Optional[int]=..., max_ticks_crossed: _Optional[int]=...) -> None:
        ...

class CosmwasmPoolInfo(_message.Message):
    __slots__ = ['weight_maps']
    WEIGHT_MAPS_FIELD_NUMBER: _ClassVar[int]
    weight_maps: _containers.RepeatedCompositeFieldContainer[WeightMap]

    def __init__(self, weight_maps: _Optional[_Iterable[_Union[WeightMap, _Mapping]]]=...) -> None:
        ...

class WeightMap(_message.Message):
    __slots__ = ['weight', 'contract_address']
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    weight: int
    contract_address: str

    def __init__(self, weight: _Optional[int]=..., contract_address: _Optional[str]=...) -> None:
        ...

class BaseDenom(_message.Message):
    __slots__ = ['denom', 'step_size']
    DENOM_FIELD_NUMBER: _ClassVar[int]
    STEP_SIZE_FIELD_NUMBER: _ClassVar[int]
    denom: str
    step_size: str

    def __init__(self, denom: _Optional[str]=..., step_size: _Optional[str]=...) -> None:
        ...

class AllProtocolRevenue(_message.Message):
    __slots__ = ['taker_fees_tracker', 'tx_fees_tracker', 'cyclic_arb_tracker']
    TAKER_FEES_TRACKER_FIELD_NUMBER: _ClassVar[int]
    TX_FEES_TRACKER_FIELD_NUMBER: _ClassVar[int]
    CYCLIC_ARB_TRACKER_FIELD_NUMBER: _ClassVar[int]
    taker_fees_tracker: _genesis_pb2.TakerFeesTracker
    tx_fees_tracker: _genesis_pb2_1.TxFeesTracker
    cyclic_arb_tracker: CyclicArbTracker

    def __init__(self, taker_fees_tracker: _Optional[_Union[_genesis_pb2.TakerFeesTracker, _Mapping]]=..., tx_fees_tracker: _Optional[_Union[_genesis_pb2_1.TxFeesTracker, _Mapping]]=..., cyclic_arb_tracker: _Optional[_Union[CyclicArbTracker, _Mapping]]=...) -> None:
        ...

class CyclicArbTracker(_message.Message):
    __slots__ = ['cyclic_arb', 'height_accounting_starts_from']
    CYCLIC_ARB_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_ACCOUNTING_STARTS_FROM_FIELD_NUMBER: _ClassVar[int]
    cyclic_arb: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    height_accounting_starts_from: int

    def __init__(self, cyclic_arb: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=..., height_accounting_starts_from: _Optional[int]=...) -> None:
        ...