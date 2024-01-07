from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class Minter(_message.Message):
    __slots__ = ['epoch_provisions']
    EPOCH_PROVISIONS_FIELD_NUMBER: _ClassVar[int]
    epoch_provisions: str

    def __init__(self, epoch_provisions: _Optional[str]=...) -> None:
        ...

class WeightedAddress(_message.Message):
    __slots__ = ['address', 'weight']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    address: str
    weight: str

    def __init__(self, address: _Optional[str]=..., weight: _Optional[str]=...) -> None:
        ...

class DistributionProportions(_message.Message):
    __slots__ = ['staking', 'pool_incentives', 'developer_rewards', 'community_pool']
    STAKING_FIELD_NUMBER: _ClassVar[int]
    POOL_INCENTIVES_FIELD_NUMBER: _ClassVar[int]
    DEVELOPER_REWARDS_FIELD_NUMBER: _ClassVar[int]
    COMMUNITY_POOL_FIELD_NUMBER: _ClassVar[int]
    staking: str
    pool_incentives: str
    developer_rewards: str
    community_pool: str

    def __init__(self, staking: _Optional[str]=..., pool_incentives: _Optional[str]=..., developer_rewards: _Optional[str]=..., community_pool: _Optional[str]=...) -> None:
        ...

class Params(_message.Message):
    __slots__ = ['mint_denom', 'genesis_epoch_provisions', 'epoch_identifier', 'reduction_period_in_epochs', 'reduction_factor', 'distribution_proportions', 'weighted_developer_rewards_receivers', 'minting_rewards_distribution_start_epoch']
    MINT_DENOM_FIELD_NUMBER: _ClassVar[int]
    GENESIS_EPOCH_PROVISIONS_FIELD_NUMBER: _ClassVar[int]
    EPOCH_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    REDUCTION_PERIOD_IN_EPOCHS_FIELD_NUMBER: _ClassVar[int]
    REDUCTION_FACTOR_FIELD_NUMBER: _ClassVar[int]
    DISTRIBUTION_PROPORTIONS_FIELD_NUMBER: _ClassVar[int]
    WEIGHTED_DEVELOPER_REWARDS_RECEIVERS_FIELD_NUMBER: _ClassVar[int]
    MINTING_REWARDS_DISTRIBUTION_START_EPOCH_FIELD_NUMBER: _ClassVar[int]
    mint_denom: str
    genesis_epoch_provisions: str
    epoch_identifier: str
    reduction_period_in_epochs: int
    reduction_factor: str
    distribution_proportions: DistributionProportions
    weighted_developer_rewards_receivers: _containers.RepeatedCompositeFieldContainer[WeightedAddress]
    minting_rewards_distribution_start_epoch: int

    def __init__(self, mint_denom: _Optional[str]=..., genesis_epoch_provisions: _Optional[str]=..., epoch_identifier: _Optional[str]=..., reduction_period_in_epochs: _Optional[int]=..., reduction_factor: _Optional[str]=..., distribution_proportions: _Optional[_Union[DistributionProportions, _Mapping]]=..., weighted_developer_rewards_receivers: _Optional[_Iterable[_Union[WeightedAddress, _Mapping]]]=..., minting_rewards_distribution_start_epoch: _Optional[int]=...) -> None:
        ...