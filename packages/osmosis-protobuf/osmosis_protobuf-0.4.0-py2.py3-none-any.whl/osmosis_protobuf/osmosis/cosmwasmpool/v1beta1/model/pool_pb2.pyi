from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class CosmWasmPool(_message.Message):
    __slots__ = ['contract_address', 'pool_id', 'code_id', 'instantiate_msg']
    CONTRACT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    CODE_ID_FIELD_NUMBER: _ClassVar[int]
    INSTANTIATE_MSG_FIELD_NUMBER: _ClassVar[int]
    contract_address: str
    pool_id: int
    code_id: int
    instantiate_msg: bytes

    def __init__(self, contract_address: _Optional[str]=..., pool_id: _Optional[int]=..., code_id: _Optional[int]=..., instantiate_msg: _Optional[bytes]=...) -> None:
        ...