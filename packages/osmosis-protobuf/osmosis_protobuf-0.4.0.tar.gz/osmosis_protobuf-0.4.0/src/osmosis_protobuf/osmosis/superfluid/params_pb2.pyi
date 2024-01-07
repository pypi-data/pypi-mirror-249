from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class Params(_message.Message):
    __slots__ = ['minimum_risk_factor']
    MINIMUM_RISK_FACTOR_FIELD_NUMBER: _ClassVar[int]
    minimum_risk_factor: str

    def __init__(self, minimum_risk_factor: _Optional[str]=...) -> None:
        ...