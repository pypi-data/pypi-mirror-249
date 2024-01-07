from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class UploadCosmWasmPoolCodeAndWhiteListProposal(_message.Message):
    __slots__ = ['title', 'description', 'wasm_byte_code']
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    WASM_BYTE_CODE_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    wasm_byte_code: bytes

    def __init__(self, title: _Optional[str]=..., description: _Optional[str]=..., wasm_byte_code: _Optional[bytes]=...) -> None:
        ...

class MigratePoolContractsProposal(_message.Message):
    __slots__ = ['title', 'description', 'pool_ids', 'new_code_id', 'wasm_byte_code', 'migrate_msg']
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    POOL_IDS_FIELD_NUMBER: _ClassVar[int]
    NEW_CODE_ID_FIELD_NUMBER: _ClassVar[int]
    WASM_BYTE_CODE_FIELD_NUMBER: _ClassVar[int]
    MIGRATE_MSG_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    pool_ids: _containers.RepeatedScalarFieldContainer[int]
    new_code_id: int
    wasm_byte_code: bytes
    migrate_msg: bytes

    def __init__(self, title: _Optional[str]=..., description: _Optional[str]=..., pool_ids: _Optional[_Iterable[int]]=..., new_code_id: _Optional[int]=..., wasm_byte_code: _Optional[bytes]=..., migrate_msg: _Optional[bytes]=...) -> None:
        ...