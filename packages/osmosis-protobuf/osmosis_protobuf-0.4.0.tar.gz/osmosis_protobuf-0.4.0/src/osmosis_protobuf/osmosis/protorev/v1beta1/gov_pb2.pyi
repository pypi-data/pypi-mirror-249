from amino import amino_pb2 as _amino_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from osmosis.protorev.v1beta1 import protorev_pb2 as _protorev_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class SetProtoRevEnabledProposal(_message.Message):
    __slots__ = ['title', 'description', 'enabled']
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    enabled: bool

    def __init__(self, title: _Optional[str]=..., description: _Optional[str]=..., enabled: bool=...) -> None:
        ...

class SetProtoRevAdminAccountProposal(_message.Message):
    __slots__ = ['title', 'description', 'account']
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    account: str

    def __init__(self, title: _Optional[str]=..., description: _Optional[str]=..., account: _Optional[str]=...) -> None:
        ...