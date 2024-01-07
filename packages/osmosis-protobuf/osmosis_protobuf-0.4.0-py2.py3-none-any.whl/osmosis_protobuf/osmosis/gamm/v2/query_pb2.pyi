from gogoproto import gogo_pb2 as _gogo_pb2
from osmosis.gamm.v1beta1 import tx_pb2 as _tx_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import any_pb2 as _any_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class QuerySpotPriceRequest(_message.Message):
    __slots__ = ['pool_id', 'base_asset_denom', 'quote_asset_denom']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    BASE_ASSET_DENOM_FIELD_NUMBER: _ClassVar[int]
    QUOTE_ASSET_DENOM_FIELD_NUMBER: _ClassVar[int]
    pool_id: int
    base_asset_denom: str
    quote_asset_denom: str

    def __init__(self, pool_id: _Optional[int]=..., base_asset_denom: _Optional[str]=..., quote_asset_denom: _Optional[str]=...) -> None:
        ...

class QuerySpotPriceResponse(_message.Message):
    __slots__ = ['spot_price']
    SPOT_PRICE_FIELD_NUMBER: _ClassVar[int]
    spot_price: str

    def __init__(self, spot_price: _Optional[str]=...) -> None:
        ...