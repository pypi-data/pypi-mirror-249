from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class EmptyRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class JoinPoolExecuteMsgRequest(_message.Message):
    __slots__ = ['join_pool']
    JOIN_POOL_FIELD_NUMBER: _ClassVar[int]
    join_pool: EmptyRequest

    def __init__(self, join_pool: _Optional[_Union[EmptyRequest, _Mapping]]=...) -> None:
        ...

class JoinPoolExecuteMsgResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class ExitPoolExecuteMsgRequest(_message.Message):
    __slots__ = ['exit_pool']
    EXIT_POOL_FIELD_NUMBER: _ClassVar[int]
    exit_pool: EmptyRequest

    def __init__(self, exit_pool: _Optional[_Union[EmptyRequest, _Mapping]]=...) -> None:
        ...

class ExitPoolExecuteMsgResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...