from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from osmosis.txfees.v1beta1 import feetoken_pb2 as _feetoken_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class QueryFeeTokensRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryFeeTokensResponse(_message.Message):
    __slots__ = ['fee_tokens']
    FEE_TOKENS_FIELD_NUMBER: _ClassVar[int]
    fee_tokens: _containers.RepeatedCompositeFieldContainer[_feetoken_pb2.FeeToken]

    def __init__(self, fee_tokens: _Optional[_Iterable[_Union[_feetoken_pb2.FeeToken, _Mapping]]]=...) -> None:
        ...

class QueryDenomSpotPriceRequest(_message.Message):
    __slots__ = ['denom']
    DENOM_FIELD_NUMBER: _ClassVar[int]
    denom: str

    def __init__(self, denom: _Optional[str]=...) -> None:
        ...

class QueryDenomSpotPriceResponse(_message.Message):
    __slots__ = ['poolID', 'spot_price']
    POOLID_FIELD_NUMBER: _ClassVar[int]
    SPOT_PRICE_FIELD_NUMBER: _ClassVar[int]
    poolID: int
    spot_price: str

    def __init__(self, poolID: _Optional[int]=..., spot_price: _Optional[str]=...) -> None:
        ...

class QueryDenomPoolIdRequest(_message.Message):
    __slots__ = ['denom']
    DENOM_FIELD_NUMBER: _ClassVar[int]
    denom: str

    def __init__(self, denom: _Optional[str]=...) -> None:
        ...

class QueryDenomPoolIdResponse(_message.Message):
    __slots__ = ['poolID']
    POOLID_FIELD_NUMBER: _ClassVar[int]
    poolID: int

    def __init__(self, poolID: _Optional[int]=...) -> None:
        ...

class QueryBaseDenomRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryBaseDenomResponse(_message.Message):
    __slots__ = ['base_denom']
    BASE_DENOM_FIELD_NUMBER: _ClassVar[int]
    base_denom: str

    def __init__(self, base_denom: _Optional[str]=...) -> None:
        ...

class QueryEipBaseFeeRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryEipBaseFeeResponse(_message.Message):
    __slots__ = ['base_fee']
    BASE_FEE_FIELD_NUMBER: _ClassVar[int]
    base_fee: str

    def __init__(self, base_fee: _Optional[str]=...) -> None:
        ...