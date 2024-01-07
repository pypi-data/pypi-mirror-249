from gogoproto import gogo_pb2 as _gogo_pb2
from osmosis.twap.v1beta1 import twap_record_pb2 as _twap_record_pb2
from osmosis.twap.v1beta1 import genesis_pb2 as _genesis_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import any_pb2 as _any_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class ArithmeticTwapRequest(_message.Message):
    __slots__ = ['pool_id', 'base_asset', 'quote_asset', 'start_time', 'end_time']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    BASE_ASSET_FIELD_NUMBER: _ClassVar[int]
    QUOTE_ASSET_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    pool_id: int
    base_asset: str
    quote_asset: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp

    def __init__(self, pool_id: _Optional[int]=..., base_asset: _Optional[str]=..., quote_asset: _Optional[str]=..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
        ...

class ArithmeticTwapResponse(_message.Message):
    __slots__ = ['arithmetic_twap']
    ARITHMETIC_TWAP_FIELD_NUMBER: _ClassVar[int]
    arithmetic_twap: str

    def __init__(self, arithmetic_twap: _Optional[str]=...) -> None:
        ...

class ArithmeticTwapToNowRequest(_message.Message):
    __slots__ = ['pool_id', 'base_asset', 'quote_asset', 'start_time']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    BASE_ASSET_FIELD_NUMBER: _ClassVar[int]
    QUOTE_ASSET_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    pool_id: int
    base_asset: str
    quote_asset: str
    start_time: _timestamp_pb2.Timestamp

    def __init__(self, pool_id: _Optional[int]=..., base_asset: _Optional[str]=..., quote_asset: _Optional[str]=..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
        ...

class ArithmeticTwapToNowResponse(_message.Message):
    __slots__ = ['arithmetic_twap']
    ARITHMETIC_TWAP_FIELD_NUMBER: _ClassVar[int]
    arithmetic_twap: str

    def __init__(self, arithmetic_twap: _Optional[str]=...) -> None:
        ...

class GeometricTwapRequest(_message.Message):
    __slots__ = ['pool_id', 'base_asset', 'quote_asset', 'start_time', 'end_time']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    BASE_ASSET_FIELD_NUMBER: _ClassVar[int]
    QUOTE_ASSET_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    pool_id: int
    base_asset: str
    quote_asset: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp

    def __init__(self, pool_id: _Optional[int]=..., base_asset: _Optional[str]=..., quote_asset: _Optional[str]=..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
        ...

class GeometricTwapResponse(_message.Message):
    __slots__ = ['geometric_twap']
    GEOMETRIC_TWAP_FIELD_NUMBER: _ClassVar[int]
    geometric_twap: str

    def __init__(self, geometric_twap: _Optional[str]=...) -> None:
        ...

class GeometricTwapToNowRequest(_message.Message):
    __slots__ = ['pool_id', 'base_asset', 'quote_asset', 'start_time']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    BASE_ASSET_FIELD_NUMBER: _ClassVar[int]
    QUOTE_ASSET_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    pool_id: int
    base_asset: str
    quote_asset: str
    start_time: _timestamp_pb2.Timestamp

    def __init__(self, pool_id: _Optional[int]=..., base_asset: _Optional[str]=..., quote_asset: _Optional[str]=..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
        ...

class GeometricTwapToNowResponse(_message.Message):
    __slots__ = ['geometric_twap']
    GEOMETRIC_TWAP_FIELD_NUMBER: _ClassVar[int]
    geometric_twap: str

    def __init__(self, geometric_twap: _Optional[str]=...) -> None:
        ...

class ParamsRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class ParamsResponse(_message.Message):
    __slots__ = ['params']
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: _genesis_pb2.Params

    def __init__(self, params: _Optional[_Union[_genesis_pb2.Params, _Mapping]]=...) -> None:
        ...