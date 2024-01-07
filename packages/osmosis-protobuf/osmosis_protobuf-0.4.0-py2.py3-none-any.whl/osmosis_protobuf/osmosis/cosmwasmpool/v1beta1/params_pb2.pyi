from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class Params(_message.Message):
    __slots__ = ['code_id_whitelist', 'pool_migration_limit']
    CODE_ID_WHITELIST_FIELD_NUMBER: _ClassVar[int]
    POOL_MIGRATION_LIMIT_FIELD_NUMBER: _ClassVar[int]
    code_id_whitelist: _containers.RepeatedScalarFieldContainer[int]
    pool_migration_limit: int

    def __init__(self, code_id_whitelist: _Optional[_Iterable[int]]=..., pool_migration_limit: _Optional[int]=...) -> None:
        ...