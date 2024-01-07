from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from amino import amino_pb2 as _amino_pb2
from osmosis.txfees.v1beta1 import feetoken_pb2 as _feetoken_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class UpdateFeeTokenProposal(_message.Message):
    __slots__ = ['title', 'description', 'feetokens']
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FEETOKENS_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    feetokens: _containers.RepeatedCompositeFieldContainer[_feetoken_pb2.FeeToken]

    def __init__(self, title: _Optional[str]=..., description: _Optional[str]=..., feetokens: _Optional[_Iterable[_Union[_feetoken_pb2.FeeToken, _Mapping]]]=...) -> None:
        ...