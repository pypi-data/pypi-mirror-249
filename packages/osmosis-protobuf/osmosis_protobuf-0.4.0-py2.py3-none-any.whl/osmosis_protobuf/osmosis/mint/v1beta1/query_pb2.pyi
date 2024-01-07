from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from osmosis.mint.v1beta1 import mint_pb2 as _mint_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class QueryParamsRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryParamsResponse(_message.Message):
    __slots__ = ['params']
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: _mint_pb2.Params

    def __init__(self, params: _Optional[_Union[_mint_pb2.Params, _Mapping]]=...) -> None:
        ...

class QueryEpochProvisionsRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryEpochProvisionsResponse(_message.Message):
    __slots__ = ['epoch_provisions']
    EPOCH_PROVISIONS_FIELD_NUMBER: _ClassVar[int]
    epoch_provisions: bytes

    def __init__(self, epoch_provisions: _Optional[bytes]=...) -> None:
        ...