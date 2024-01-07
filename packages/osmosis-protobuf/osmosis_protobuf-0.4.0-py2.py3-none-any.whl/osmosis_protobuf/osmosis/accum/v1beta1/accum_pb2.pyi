from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class AccumulatorContent(_message.Message):
    __slots__ = ['accum_value', 'total_shares']
    ACCUM_VALUE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SHARES_FIELD_NUMBER: _ClassVar[int]
    accum_value: _containers.RepeatedCompositeFieldContainer[_coin_pb2.DecCoin]
    total_shares: str

    def __init__(self, accum_value: _Optional[_Iterable[_Union[_coin_pb2.DecCoin, _Mapping]]]=..., total_shares: _Optional[str]=...) -> None:
        ...

class Options(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class Record(_message.Message):
    __slots__ = ['num_shares', 'accum_value_per_share', 'unclaimed_rewards_total', 'options']
    NUM_SHARES_FIELD_NUMBER: _ClassVar[int]
    ACCUM_VALUE_PER_SHARE_FIELD_NUMBER: _ClassVar[int]
    UNCLAIMED_REWARDS_TOTAL_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    num_shares: str
    accum_value_per_share: _containers.RepeatedCompositeFieldContainer[_coin_pb2.DecCoin]
    unclaimed_rewards_total: _containers.RepeatedCompositeFieldContainer[_coin_pb2.DecCoin]
    options: Options

    def __init__(self, num_shares: _Optional[str]=..., accum_value_per_share: _Optional[_Iterable[_Union[_coin_pb2.DecCoin, _Mapping]]]=..., unclaimed_rewards_total: _Optional[_Iterable[_Union[_coin_pb2.DecCoin, _Mapping]]]=..., options: _Optional[_Union[Options, _Mapping]]=...) -> None:
        ...