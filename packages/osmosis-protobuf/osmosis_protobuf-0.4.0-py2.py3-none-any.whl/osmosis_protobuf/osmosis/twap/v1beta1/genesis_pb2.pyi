from gogoproto import gogo_pb2 as _gogo_pb2
from osmosis.twap.v1beta1 import twap_record_pb2 as _twap_record_pb2
from google.protobuf import any_pb2 as _any_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class Params(_message.Message):
    __slots__ = ['prune_epoch_identifier', 'record_history_keep_period']
    PRUNE_EPOCH_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    RECORD_HISTORY_KEEP_PERIOD_FIELD_NUMBER: _ClassVar[int]
    prune_epoch_identifier: str
    record_history_keep_period: _duration_pb2.Duration

    def __init__(self, prune_epoch_identifier: _Optional[str]=..., record_history_keep_period: _Optional[_Union[_duration_pb2.Duration, _Mapping]]=...) -> None:
        ...

class GenesisState(_message.Message):
    __slots__ = ['twaps', 'params']
    TWAPS_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    twaps: _containers.RepeatedCompositeFieldContainer[_twap_record_pb2.TwapRecord]
    params: Params

    def __init__(self, twaps: _Optional[_Iterable[_Union[_twap_record_pb2.TwapRecord, _Mapping]]]=..., params: _Optional[_Union[Params, _Mapping]]=...) -> None:
        ...