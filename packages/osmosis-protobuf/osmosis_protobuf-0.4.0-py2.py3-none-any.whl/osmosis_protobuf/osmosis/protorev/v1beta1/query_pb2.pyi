from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from osmosis.protorev.v1beta1 import params_pb2 as _params_pb2
from osmosis.protorev.v1beta1 import protorev_pb2 as _protorev_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class QueryParamsRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryParamsResponse(_message.Message):
    __slots__ = ['params']
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: _params_pb2.Params

    def __init__(self, params: _Optional[_Union[_params_pb2.Params, _Mapping]]=...) -> None:
        ...

class QueryGetProtoRevNumberOfTradesRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryGetProtoRevNumberOfTradesResponse(_message.Message):
    __slots__ = ['number_of_trades']
    NUMBER_OF_TRADES_FIELD_NUMBER: _ClassVar[int]
    number_of_trades: str

    def __init__(self, number_of_trades: _Optional[str]=...) -> None:
        ...

class QueryGetProtoRevProfitsByDenomRequest(_message.Message):
    __slots__ = ['denom']
    DENOM_FIELD_NUMBER: _ClassVar[int]
    denom: str

    def __init__(self, denom: _Optional[str]=...) -> None:
        ...

class QueryGetProtoRevProfitsByDenomResponse(_message.Message):
    __slots__ = ['profit']
    PROFIT_FIELD_NUMBER: _ClassVar[int]
    profit: _coin_pb2.Coin

    def __init__(self, profit: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=...) -> None:
        ...

class QueryGetProtoRevAllProfitsRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryGetProtoRevAllProfitsResponse(_message.Message):
    __slots__ = ['profits']
    PROFITS_FIELD_NUMBER: _ClassVar[int]
    profits: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, profits: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class QueryGetProtoRevStatisticsByRouteRequest(_message.Message):
    __slots__ = ['route']
    ROUTE_FIELD_NUMBER: _ClassVar[int]
    route: _containers.RepeatedScalarFieldContainer[int]

    def __init__(self, route: _Optional[_Iterable[int]]=...) -> None:
        ...

class QueryGetProtoRevStatisticsByRouteResponse(_message.Message):
    __slots__ = ['statistics']
    STATISTICS_FIELD_NUMBER: _ClassVar[int]
    statistics: _protorev_pb2.RouteStatistics

    def __init__(self, statistics: _Optional[_Union[_protorev_pb2.RouteStatistics, _Mapping]]=...) -> None:
        ...

class QueryGetProtoRevAllRouteStatisticsRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryGetProtoRevAllRouteStatisticsResponse(_message.Message):
    __slots__ = ['statistics']
    STATISTICS_FIELD_NUMBER: _ClassVar[int]
    statistics: _containers.RepeatedCompositeFieldContainer[_protorev_pb2.RouteStatistics]

    def __init__(self, statistics: _Optional[_Iterable[_Union[_protorev_pb2.RouteStatistics, _Mapping]]]=...) -> None:
        ...

class QueryGetProtoRevTokenPairArbRoutesRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryGetProtoRevTokenPairArbRoutesResponse(_message.Message):
    __slots__ = ['routes']
    ROUTES_FIELD_NUMBER: _ClassVar[int]
    routes: _containers.RepeatedCompositeFieldContainer[_protorev_pb2.TokenPairArbRoutes]

    def __init__(self, routes: _Optional[_Iterable[_Union[_protorev_pb2.TokenPairArbRoutes, _Mapping]]]=...) -> None:
        ...

class QueryGetProtoRevAdminAccountRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryGetProtoRevAdminAccountResponse(_message.Message):
    __slots__ = ['admin_account']
    ADMIN_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    admin_account: str

    def __init__(self, admin_account: _Optional[str]=...) -> None:
        ...

class QueryGetProtoRevDeveloperAccountRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryGetProtoRevDeveloperAccountResponse(_message.Message):
    __slots__ = ['developer_account']
    DEVELOPER_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    developer_account: str

    def __init__(self, developer_account: _Optional[str]=...) -> None:
        ...

class QueryGetProtoRevInfoByPoolTypeRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryGetProtoRevInfoByPoolTypeResponse(_message.Message):
    __slots__ = ['info_by_pool_type']
    INFO_BY_POOL_TYPE_FIELD_NUMBER: _ClassVar[int]
    info_by_pool_type: _protorev_pb2.InfoByPoolType

    def __init__(self, info_by_pool_type: _Optional[_Union[_protorev_pb2.InfoByPoolType, _Mapping]]=...) -> None:
        ...

class QueryGetProtoRevMaxPoolPointsPerBlockRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryGetProtoRevMaxPoolPointsPerBlockResponse(_message.Message):
    __slots__ = ['max_pool_points_per_block']
    MAX_POOL_POINTS_PER_BLOCK_FIELD_NUMBER: _ClassVar[int]
    max_pool_points_per_block: int

    def __init__(self, max_pool_points_per_block: _Optional[int]=...) -> None:
        ...

class QueryGetProtoRevMaxPoolPointsPerTxRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryGetProtoRevMaxPoolPointsPerTxResponse(_message.Message):
    __slots__ = ['max_pool_points_per_tx']
    MAX_POOL_POINTS_PER_TX_FIELD_NUMBER: _ClassVar[int]
    max_pool_points_per_tx: int

    def __init__(self, max_pool_points_per_tx: _Optional[int]=...) -> None:
        ...

class QueryGetProtoRevBaseDenomsRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryGetProtoRevBaseDenomsResponse(_message.Message):
    __slots__ = ['base_denoms']
    BASE_DENOMS_FIELD_NUMBER: _ClassVar[int]
    base_denoms: _containers.RepeatedCompositeFieldContainer[_protorev_pb2.BaseDenom]

    def __init__(self, base_denoms: _Optional[_Iterable[_Union[_protorev_pb2.BaseDenom, _Mapping]]]=...) -> None:
        ...

class QueryGetProtoRevEnabledRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryGetProtoRevEnabledResponse(_message.Message):
    __slots__ = ['enabled']
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    enabled: bool

    def __init__(self, enabled: bool=...) -> None:
        ...

class QueryGetProtoRevPoolRequest(_message.Message):
    __slots__ = ['base_denom', 'other_denom']
    BASE_DENOM_FIELD_NUMBER: _ClassVar[int]
    OTHER_DENOM_FIELD_NUMBER: _ClassVar[int]
    base_denom: str
    other_denom: str

    def __init__(self, base_denom: _Optional[str]=..., other_denom: _Optional[str]=...) -> None:
        ...

class QueryGetProtoRevPoolResponse(_message.Message):
    __slots__ = ['pool_id']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    pool_id: int

    def __init__(self, pool_id: _Optional[int]=...) -> None:
        ...

class QueryGetAllProtocolRevenueRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryGetAllProtocolRevenueResponse(_message.Message):
    __slots__ = ['all_protocol_revenue']
    ALL_PROTOCOL_REVENUE_FIELD_NUMBER: _ClassVar[int]
    all_protocol_revenue: _protorev_pb2.AllProtocolRevenue

    def __init__(self, all_protocol_revenue: _Optional[_Union[_protorev_pb2.AllProtocolRevenue, _Mapping]]=...) -> None:
        ...