from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import any_pb2 as _any_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class TwapRecord(_message.Message):
    __slots__ = ['pool_id', 'asset0_denom', 'asset1_denom', 'height', 'time', 'p0_last_spot_price', 'p1_last_spot_price', 'p0_arithmetic_twap_accumulator', 'p1_arithmetic_twap_accumulator', 'geometric_twap_accumulator', 'last_error_time']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    ASSET0_DENOM_FIELD_NUMBER: _ClassVar[int]
    ASSET1_DENOM_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    P0_LAST_SPOT_PRICE_FIELD_NUMBER: _ClassVar[int]
    P1_LAST_SPOT_PRICE_FIELD_NUMBER: _ClassVar[int]
    P0_ARITHMETIC_TWAP_ACCUMULATOR_FIELD_NUMBER: _ClassVar[int]
    P1_ARITHMETIC_TWAP_ACCUMULATOR_FIELD_NUMBER: _ClassVar[int]
    GEOMETRIC_TWAP_ACCUMULATOR_FIELD_NUMBER: _ClassVar[int]
    LAST_ERROR_TIME_FIELD_NUMBER: _ClassVar[int]
    pool_id: int
    asset0_denom: str
    asset1_denom: str
    height: int
    time: _timestamp_pb2.Timestamp
    p0_last_spot_price: str
    p1_last_spot_price: str
    p0_arithmetic_twap_accumulator: str
    p1_arithmetic_twap_accumulator: str
    geometric_twap_accumulator: str
    last_error_time: _timestamp_pb2.Timestamp

    def __init__(self, pool_id: _Optional[int]=..., asset0_denom: _Optional[str]=..., asset1_denom: _Optional[str]=..., height: _Optional[int]=..., time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., p0_last_spot_price: _Optional[str]=..., p1_last_spot_price: _Optional[str]=..., p0_arithmetic_twap_accumulator: _Optional[str]=..., p1_arithmetic_twap_accumulator: _Optional[str]=..., geometric_twap_accumulator: _Optional[str]=..., last_error_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
        ...