from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class MsgCreateCosmWasmPool(_message.Message):
    __slots__ = ['code_id', 'instantiate_msg', 'sender']
    CODE_ID_FIELD_NUMBER: _ClassVar[int]
    INSTANTIATE_MSG_FIELD_NUMBER: _ClassVar[int]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    code_id: int
    instantiate_msg: bytes
    sender: str

    def __init__(self, code_id: _Optional[int]=..., instantiate_msg: _Optional[bytes]=..., sender: _Optional[str]=...) -> None:
        ...

class MsgCreateCosmWasmPoolResponse(_message.Message):
    __slots__ = ['pool_id']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    pool_id: int

    def __init__(self, pool_id: _Optional[int]=...) -> None:
        ...