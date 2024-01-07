from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from osmosis.tokenfactory.v1beta1 import authorityMetadata_pb2 as _authorityMetadata_pb2
from osmosis.tokenfactory.v1beta1 import params_pb2 as _params_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class QueryParamsRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryParamsResponse(_message.Message):
    __slots__ = ['params']
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: _params_pb2.Params

    def __init__(self, params: _Optional[_Union[_params_pb2.Params, _Mapping]]=...) -> None:
        ...

class QueryDenomAuthorityMetadataRequest(_message.Message):
    __slots__ = ['denom']
    DENOM_FIELD_NUMBER: _ClassVar[int]
    denom: str

    def __init__(self, denom: _Optional[str]=...) -> None:
        ...

class QueryDenomAuthorityMetadataResponse(_message.Message):
    __slots__ = ['authority_metadata']
    AUTHORITY_METADATA_FIELD_NUMBER: _ClassVar[int]
    authority_metadata: _authorityMetadata_pb2.DenomAuthorityMetadata

    def __init__(self, authority_metadata: _Optional[_Union[_authorityMetadata_pb2.DenomAuthorityMetadata, _Mapping]]=...) -> None:
        ...

class QueryDenomsFromCreatorRequest(_message.Message):
    __slots__ = ['creator']
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    creator: str

    def __init__(self, creator: _Optional[str]=...) -> None:
        ...

class QueryDenomsFromCreatorResponse(_message.Message):
    __slots__ = ['denoms']
    DENOMS_FIELD_NUMBER: _ClassVar[int]
    denoms: _containers.RepeatedScalarFieldContainer[str]

    def __init__(self, denoms: _Optional[_Iterable[str]]=...) -> None:
        ...

class QueryBeforeSendHookAddressRequest(_message.Message):
    __slots__ = ['denom']
    DENOM_FIELD_NUMBER: _ClassVar[int]
    denom: str

    def __init__(self, denom: _Optional[str]=...) -> None:
        ...

class QueryBeforeSendHookAddressResponse(_message.Message):
    __slots__ = ['cosmwasm_address']
    COSMWASM_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    cosmwasm_address: str

    def __init__(self, cosmwasm_address: _Optional[str]=...) -> None:
        ...