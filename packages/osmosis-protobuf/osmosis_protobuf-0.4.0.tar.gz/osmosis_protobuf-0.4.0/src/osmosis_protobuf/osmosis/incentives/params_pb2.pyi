from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class Params(_message.Message):
    __slots__ = ['distr_epoch_identifier', 'group_creation_fee', 'unrestricted_creator_whitelist']
    DISTR_EPOCH_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    GROUP_CREATION_FEE_FIELD_NUMBER: _ClassVar[int]
    UNRESTRICTED_CREATOR_WHITELIST_FIELD_NUMBER: _ClassVar[int]
    distr_epoch_identifier: str
    group_creation_fee: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    unrestricted_creator_whitelist: _containers.RepeatedScalarFieldContainer[str]

    def __init__(self, distr_epoch_identifier: _Optional[str]=..., group_creation_fee: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=..., unrestricted_creator_whitelist: _Optional[_Iterable[str]]=...) -> None:
        ...