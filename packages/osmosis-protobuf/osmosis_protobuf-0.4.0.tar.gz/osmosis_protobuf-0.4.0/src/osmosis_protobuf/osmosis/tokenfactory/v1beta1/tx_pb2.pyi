from gogoproto import gogo_pb2 as _gogo_pb2
from amino import amino_pb2 as _amino_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from cosmos.bank.v1beta1 import bank_pb2 as _bank_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class MsgCreateDenom(_message.Message):
    __slots__ = ['sender', 'subdenom']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    SUBDENOM_FIELD_NUMBER: _ClassVar[int]
    sender: str
    subdenom: str

    def __init__(self, sender: _Optional[str]=..., subdenom: _Optional[str]=...) -> None:
        ...

class MsgCreateDenomResponse(_message.Message):
    __slots__ = ['new_token_denom']
    NEW_TOKEN_DENOM_FIELD_NUMBER: _ClassVar[int]
    new_token_denom: str

    def __init__(self, new_token_denom: _Optional[str]=...) -> None:
        ...

class MsgMint(_message.Message):
    __slots__ = ['sender', 'amount', 'mintToAddress']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    MINTTOADDRESS_FIELD_NUMBER: _ClassVar[int]
    sender: str
    amount: _coin_pb2.Coin
    mintToAddress: str

    def __init__(self, sender: _Optional[str]=..., amount: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=..., mintToAddress: _Optional[str]=...) -> None:
        ...

class MsgMintResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgBurn(_message.Message):
    __slots__ = ['sender', 'amount', 'burnFromAddress']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    BURNFROMADDRESS_FIELD_NUMBER: _ClassVar[int]
    sender: str
    amount: _coin_pb2.Coin
    burnFromAddress: str

    def __init__(self, sender: _Optional[str]=..., amount: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=..., burnFromAddress: _Optional[str]=...) -> None:
        ...

class MsgBurnResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgChangeAdmin(_message.Message):
    __slots__ = ['sender', 'denom', 'new_admin']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    DENOM_FIELD_NUMBER: _ClassVar[int]
    NEW_ADMIN_FIELD_NUMBER: _ClassVar[int]
    sender: str
    denom: str
    new_admin: str

    def __init__(self, sender: _Optional[str]=..., denom: _Optional[str]=..., new_admin: _Optional[str]=...) -> None:
        ...

class MsgChangeAdminResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgSetBeforeSendHook(_message.Message):
    __slots__ = ['sender', 'denom', 'cosmwasm_address']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    DENOM_FIELD_NUMBER: _ClassVar[int]
    COSMWASM_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    sender: str
    denom: str
    cosmwasm_address: str

    def __init__(self, sender: _Optional[str]=..., denom: _Optional[str]=..., cosmwasm_address: _Optional[str]=...) -> None:
        ...

class MsgSetBeforeSendHookResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgSetDenomMetadata(_message.Message):
    __slots__ = ['sender', 'metadata']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    sender: str
    metadata: _bank_pb2.Metadata

    def __init__(self, sender: _Optional[str]=..., metadata: _Optional[_Union[_bank_pb2.Metadata, _Mapping]]=...) -> None:
        ...

class MsgSetDenomMetadataResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgForceTransfer(_message.Message):
    __slots__ = ['sender', 'amount', 'transferFromAddress', 'transferToAddress']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    TRANSFERFROMADDRESS_FIELD_NUMBER: _ClassVar[int]
    TRANSFERTOADDRESS_FIELD_NUMBER: _ClassVar[int]
    sender: str
    amount: _coin_pb2.Coin
    transferFromAddress: str
    transferToAddress: str

    def __init__(self, sender: _Optional[str]=..., amount: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=..., transferFromAddress: _Optional[str]=..., transferToAddress: _Optional[str]=...) -> None:
        ...

class MsgForceTransferResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...