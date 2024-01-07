from gogoproto import gogo_pb2 as _gogo_pb2
from amino import amino_pb2 as _amino_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from osmosis.incentives import gauge_pb2 as _gauge_pb2
from osmosis.lockup import lock_pb2 as _lock_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class MsgCreateGauge(_message.Message):
    __slots__ = ['is_perpetual', 'owner', 'distribute_to', 'coins', 'start_time', 'num_epochs_paid_over', 'pool_id']
    IS_PERPETUAL_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    DISTRIBUTE_TO_FIELD_NUMBER: _ClassVar[int]
    COINS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    NUM_EPOCHS_PAID_OVER_FIELD_NUMBER: _ClassVar[int]
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    is_perpetual: bool
    owner: str
    distribute_to: _lock_pb2.QueryCondition
    coins: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    start_time: _timestamp_pb2.Timestamp
    num_epochs_paid_over: int
    pool_id: int

    def __init__(self, is_perpetual: bool=..., owner: _Optional[str]=..., distribute_to: _Optional[_Union[_lock_pb2.QueryCondition, _Mapping]]=..., coins: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., num_epochs_paid_over: _Optional[int]=..., pool_id: _Optional[int]=...) -> None:
        ...

class MsgCreateGaugeResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgAddToGauge(_message.Message):
    __slots__ = ['owner', 'gauge_id', 'rewards']
    OWNER_FIELD_NUMBER: _ClassVar[int]
    GAUGE_ID_FIELD_NUMBER: _ClassVar[int]
    REWARDS_FIELD_NUMBER: _ClassVar[int]
    owner: str
    gauge_id: int
    rewards: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, owner: _Optional[str]=..., gauge_id: _Optional[int]=..., rewards: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class MsgAddToGaugeResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgCreateGroup(_message.Message):
    __slots__ = ['coins', 'num_epochs_paid_over', 'owner', 'pool_ids']
    COINS_FIELD_NUMBER: _ClassVar[int]
    NUM_EPOCHS_PAID_OVER_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    POOL_IDS_FIELD_NUMBER: _ClassVar[int]
    coins: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    num_epochs_paid_over: int
    owner: str
    pool_ids: _containers.RepeatedScalarFieldContainer[int]

    def __init__(self, coins: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=..., num_epochs_paid_over: _Optional[int]=..., owner: _Optional[str]=..., pool_ids: _Optional[_Iterable[int]]=...) -> None:
        ...

class MsgCreateGroupResponse(_message.Message):
    __slots__ = ['group_id']
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    group_id: int

    def __init__(self, group_id: _Optional[int]=...) -> None:
        ...