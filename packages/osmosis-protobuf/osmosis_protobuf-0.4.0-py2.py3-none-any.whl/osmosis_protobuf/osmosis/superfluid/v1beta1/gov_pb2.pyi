from gogoproto import gogo_pb2 as _gogo_pb2
from amino import amino_pb2 as _amino_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from osmosis.superfluid import superfluid_pb2 as _superfluid_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class SetSuperfluidAssetsProposal(_message.Message):
    __slots__ = ['title', 'description', 'assets']
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ASSETS_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    assets: _containers.RepeatedCompositeFieldContainer[_superfluid_pb2.SuperfluidAsset]

    def __init__(self, title: _Optional[str]=..., description: _Optional[str]=..., assets: _Optional[_Iterable[_Union[_superfluid_pb2.SuperfluidAsset, _Mapping]]]=...) -> None:
        ...

class RemoveSuperfluidAssetsProposal(_message.Message):
    __slots__ = ['title', 'description', 'superfluid_asset_denoms']
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SUPERFLUID_ASSET_DENOMS_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    superfluid_asset_denoms: _containers.RepeatedScalarFieldContainer[str]

    def __init__(self, title: _Optional[str]=..., description: _Optional[str]=..., superfluid_asset_denoms: _Optional[_Iterable[str]]=...) -> None:
        ...

class UpdateUnpoolWhiteListProposal(_message.Message):
    __slots__ = ['title', 'description', 'ids', 'is_overwrite']
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IDS_FIELD_NUMBER: _ClassVar[int]
    IS_OVERWRITE_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    ids: _containers.RepeatedScalarFieldContainer[int]
    is_overwrite: bool

    def __init__(self, title: _Optional[str]=..., description: _Optional[str]=..., ids: _Optional[_Iterable[int]]=..., is_overwrite: bool=...) -> None:
        ...