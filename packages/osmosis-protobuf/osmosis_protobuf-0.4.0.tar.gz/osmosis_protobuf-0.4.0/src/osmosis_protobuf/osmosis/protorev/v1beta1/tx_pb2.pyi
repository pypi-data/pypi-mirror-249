from gogoproto import gogo_pb2 as _gogo_pb2
from amino import amino_pb2 as _amino_pb2
from google.api import annotations_pb2 as _annotations_pb2
from osmosis.protorev.v1beta1 import protorev_pb2 as _protorev_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class MsgSetHotRoutes(_message.Message):
    __slots__ = ['admin', 'hot_routes']
    ADMIN_FIELD_NUMBER: _ClassVar[int]
    HOT_ROUTES_FIELD_NUMBER: _ClassVar[int]
    admin: str
    hot_routes: _containers.RepeatedCompositeFieldContainer[_protorev_pb2.TokenPairArbRoutes]

    def __init__(self, admin: _Optional[str]=..., hot_routes: _Optional[_Iterable[_Union[_protorev_pb2.TokenPairArbRoutes, _Mapping]]]=...) -> None:
        ...

class MsgSetHotRoutesResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgSetDeveloperAccount(_message.Message):
    __slots__ = ['admin', 'developer_account']
    ADMIN_FIELD_NUMBER: _ClassVar[int]
    DEVELOPER_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    admin: str
    developer_account: str

    def __init__(self, admin: _Optional[str]=..., developer_account: _Optional[str]=...) -> None:
        ...

class MsgSetDeveloperAccountResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgSetInfoByPoolType(_message.Message):
    __slots__ = ['admin', 'info_by_pool_type']
    ADMIN_FIELD_NUMBER: _ClassVar[int]
    INFO_BY_POOL_TYPE_FIELD_NUMBER: _ClassVar[int]
    admin: str
    info_by_pool_type: _protorev_pb2.InfoByPoolType

    def __init__(self, admin: _Optional[str]=..., info_by_pool_type: _Optional[_Union[_protorev_pb2.InfoByPoolType, _Mapping]]=...) -> None:
        ...

class MsgSetInfoByPoolTypeResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgSetMaxPoolPointsPerTx(_message.Message):
    __slots__ = ['admin', 'max_pool_points_per_tx']
    ADMIN_FIELD_NUMBER: _ClassVar[int]
    MAX_POOL_POINTS_PER_TX_FIELD_NUMBER: _ClassVar[int]
    admin: str
    max_pool_points_per_tx: int

    def __init__(self, admin: _Optional[str]=..., max_pool_points_per_tx: _Optional[int]=...) -> None:
        ...

class MsgSetMaxPoolPointsPerTxResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgSetMaxPoolPointsPerBlock(_message.Message):
    __slots__ = ['admin', 'max_pool_points_per_block']
    ADMIN_FIELD_NUMBER: _ClassVar[int]
    MAX_POOL_POINTS_PER_BLOCK_FIELD_NUMBER: _ClassVar[int]
    admin: str
    max_pool_points_per_block: int

    def __init__(self, admin: _Optional[str]=..., max_pool_points_per_block: _Optional[int]=...) -> None:
        ...

class MsgSetMaxPoolPointsPerBlockResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgSetBaseDenoms(_message.Message):
    __slots__ = ['admin', 'base_denoms']
    ADMIN_FIELD_NUMBER: _ClassVar[int]
    BASE_DENOMS_FIELD_NUMBER: _ClassVar[int]
    admin: str
    base_denoms: _containers.RepeatedCompositeFieldContainer[_protorev_pb2.BaseDenom]

    def __init__(self, admin: _Optional[str]=..., base_denoms: _Optional[_Iterable[_Union[_protorev_pb2.BaseDenom, _Mapping]]]=...) -> None:
        ...

class MsgSetBaseDenomsResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...