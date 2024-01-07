from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class SwapExactAmountIn(_message.Message):
    __slots__ = ['sender', 'token_in', 'token_out_denom', 'token_out_min_amount', 'swap_fee']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IN_FIELD_NUMBER: _ClassVar[int]
    TOKEN_OUT_DENOM_FIELD_NUMBER: _ClassVar[int]
    TOKEN_OUT_MIN_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    SWAP_FEE_FIELD_NUMBER: _ClassVar[int]
    sender: str
    token_in: _coin_pb2.Coin
    token_out_denom: str
    token_out_min_amount: str
    swap_fee: str

    def __init__(self, sender: _Optional[str]=..., token_in: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=..., token_out_denom: _Optional[str]=..., token_out_min_amount: _Optional[str]=..., swap_fee: _Optional[str]=...) -> None:
        ...

class SwapExactAmountInSudoMsg(_message.Message):
    __slots__ = ['swap_exact_amount_in']
    SWAP_EXACT_AMOUNT_IN_FIELD_NUMBER: _ClassVar[int]
    swap_exact_amount_in: SwapExactAmountIn

    def __init__(self, swap_exact_amount_in: _Optional[_Union[SwapExactAmountIn, _Mapping]]=...) -> None:
        ...

class SwapExactAmountInSudoMsgResponse(_message.Message):
    __slots__ = ['token_out_amount']
    TOKEN_OUT_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    token_out_amount: str

    def __init__(self, token_out_amount: _Optional[str]=...) -> None:
        ...

class SwapExactAmountOut(_message.Message):
    __slots__ = ['sender', 'token_out', 'token_in_denom', 'token_in_max_amount', 'swap_fee']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    TOKEN_OUT_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IN_DENOM_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IN_MAX_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    SWAP_FEE_FIELD_NUMBER: _ClassVar[int]
    sender: str
    token_out: _coin_pb2.Coin
    token_in_denom: str
    token_in_max_amount: str
    swap_fee: str

    def __init__(self, sender: _Optional[str]=..., token_out: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=..., token_in_denom: _Optional[str]=..., token_in_max_amount: _Optional[str]=..., swap_fee: _Optional[str]=...) -> None:
        ...

class SwapExactAmountOutSudoMsg(_message.Message):
    __slots__ = ['swap_exact_amount_out']
    SWAP_EXACT_AMOUNT_OUT_FIELD_NUMBER: _ClassVar[int]
    swap_exact_amount_out: SwapExactAmountOut

    def __init__(self, swap_exact_amount_out: _Optional[_Union[SwapExactAmountOut, _Mapping]]=...) -> None:
        ...

class SwapExactAmountOutSudoMsgResponse(_message.Message):
    __slots__ = ['token_in_amount']
    TOKEN_IN_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    token_in_amount: str

    def __init__(self, token_in_amount: _Optional[str]=...) -> None:
        ...