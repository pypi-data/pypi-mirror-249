from gogoproto import gogo_pb2 as _gogo_pb2
from osmosis.gamm.v1beta1 import genesis_pb2 as _genesis_pb2
from osmosis.gamm.v1beta1 import shared_pb2 as _shared_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from amino import amino_pb2 as _amino_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class ReplaceMigrationRecordsProposal(_message.Message):
    __slots__ = ['title', 'description', 'records']
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    records: _containers.RepeatedCompositeFieldContainer[_shared_pb2.BalancerToConcentratedPoolLink]

    def __init__(self, title: _Optional[str]=..., description: _Optional[str]=..., records: _Optional[_Iterable[_Union[_shared_pb2.BalancerToConcentratedPoolLink, _Mapping]]]=...) -> None:
        ...

class UpdateMigrationRecordsProposal(_message.Message):
    __slots__ = ['title', 'description', 'records']
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    records: _containers.RepeatedCompositeFieldContainer[_shared_pb2.BalancerToConcentratedPoolLink]

    def __init__(self, title: _Optional[str]=..., description: _Optional[str]=..., records: _Optional[_Iterable[_Union[_shared_pb2.BalancerToConcentratedPoolLink, _Mapping]]]=...) -> None:
        ...

class PoolRecordWithCFMMLink(_message.Message):
    __slots__ = ['denom0', 'denom1', 'tick_spacing', 'exponent_at_price_one', 'spread_factor', 'balancer_pool_id']
    DENOM0_FIELD_NUMBER: _ClassVar[int]
    DENOM1_FIELD_NUMBER: _ClassVar[int]
    TICK_SPACING_FIELD_NUMBER: _ClassVar[int]
    EXPONENT_AT_PRICE_ONE_FIELD_NUMBER: _ClassVar[int]
    SPREAD_FACTOR_FIELD_NUMBER: _ClassVar[int]
    BALANCER_POOL_ID_FIELD_NUMBER: _ClassVar[int]
    denom0: str
    denom1: str
    tick_spacing: int
    exponent_at_price_one: str
    spread_factor: str
    balancer_pool_id: int

    def __init__(self, denom0: _Optional[str]=..., denom1: _Optional[str]=..., tick_spacing: _Optional[int]=..., exponent_at_price_one: _Optional[str]=..., spread_factor: _Optional[str]=..., balancer_pool_id: _Optional[int]=...) -> None:
        ...

class CreateConcentratedLiquidityPoolsAndLinktoCFMMProposal(_message.Message):
    __slots__ = ['title', 'description', 'pool_records_with_cfmm_link']
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    POOL_RECORDS_WITH_CFMM_LINK_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    pool_records_with_cfmm_link: _containers.RepeatedCompositeFieldContainer[PoolRecordWithCFMMLink]

    def __init__(self, title: _Optional[str]=..., description: _Optional[str]=..., pool_records_with_cfmm_link: _Optional[_Iterable[_Union[PoolRecordWithCFMMLink, _Mapping]]]=...) -> None:
        ...

class SetScalingFactorControllerProposal(_message.Message):
    __slots__ = ['title', 'description', 'pool_id', 'controller_address']
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    CONTROLLER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    pool_id: int
    controller_address: str

    def __init__(self, title: _Optional[str]=..., description: _Optional[str]=..., pool_id: _Optional[int]=..., controller_address: _Optional[str]=...) -> None:
        ...