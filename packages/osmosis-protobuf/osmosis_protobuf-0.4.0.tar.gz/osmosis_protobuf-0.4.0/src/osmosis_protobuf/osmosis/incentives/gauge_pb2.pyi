from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from osmosis.lockup import lock_pb2 as _lock_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class Gauge(_message.Message):
    __slots__ = ['id', 'is_perpetual', 'distribute_to', 'coins', 'start_time', 'num_epochs_paid_over', 'filled_epochs', 'distributed_coins']
    ID_FIELD_NUMBER: _ClassVar[int]
    IS_PERPETUAL_FIELD_NUMBER: _ClassVar[int]
    DISTRIBUTE_TO_FIELD_NUMBER: _ClassVar[int]
    COINS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    NUM_EPOCHS_PAID_OVER_FIELD_NUMBER: _ClassVar[int]
    FILLED_EPOCHS_FIELD_NUMBER: _ClassVar[int]
    DISTRIBUTED_COINS_FIELD_NUMBER: _ClassVar[int]
    id: int
    is_perpetual: bool
    distribute_to: _lock_pb2.QueryCondition
    coins: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    start_time: _timestamp_pb2.Timestamp
    num_epochs_paid_over: int
    filled_epochs: int
    distributed_coins: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, id: _Optional[int]=..., is_perpetual: bool=..., distribute_to: _Optional[_Union[_lock_pb2.QueryCondition, _Mapping]]=..., coins: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., num_epochs_paid_over: _Optional[int]=..., filled_epochs: _Optional[int]=..., distributed_coins: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class LockableDurationsInfo(_message.Message):
    __slots__ = ['lockable_durations']
    LOCKABLE_DURATIONS_FIELD_NUMBER: _ClassVar[int]
    lockable_durations: _containers.RepeatedCompositeFieldContainer[_duration_pb2.Duration]

    def __init__(self, lockable_durations: _Optional[_Iterable[_Union[_duration_pb2.Duration, _Mapping]]]=...) -> None:
        ...