from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class CalcOutAmtGivenIn(_message.Message):
    __slots__ = ['token_in', 'token_out_denom', 'swap_fee']
    TOKEN_IN_FIELD_NUMBER: _ClassVar[int]
    TOKEN_OUT_DENOM_FIELD_NUMBER: _ClassVar[int]
    SWAP_FEE_FIELD_NUMBER: _ClassVar[int]
    token_in: _coin_pb2.Coin
    token_out_denom: str
    swap_fee: str

    def __init__(self, token_in: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=..., token_out_denom: _Optional[str]=..., swap_fee: _Optional[str]=...) -> None:
        ...

class CalcOutAmtGivenInRequest(_message.Message):
    __slots__ = ['calc_out_amt_given_in']
    CALC_OUT_AMT_GIVEN_IN_FIELD_NUMBER: _ClassVar[int]
    calc_out_amt_given_in: CalcOutAmtGivenIn

    def __init__(self, calc_out_amt_given_in: _Optional[_Union[CalcOutAmtGivenIn, _Mapping]]=...) -> None:
        ...

class CalcOutAmtGivenInResponse(_message.Message):
    __slots__ = ['token_out']
    TOKEN_OUT_FIELD_NUMBER: _ClassVar[int]
    token_out: _coin_pb2.Coin

    def __init__(self, token_out: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=...) -> None:
        ...

class CalcInAmtGivenOut(_message.Message):
    __slots__ = ['token_out', 'token_in_denom', 'swap_fee']
    TOKEN_OUT_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IN_DENOM_FIELD_NUMBER: _ClassVar[int]
    SWAP_FEE_FIELD_NUMBER: _ClassVar[int]
    token_out: _coin_pb2.Coin
    token_in_denom: str
    swap_fee: str

    def __init__(self, token_out: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=..., token_in_denom: _Optional[str]=..., swap_fee: _Optional[str]=...) -> None:
        ...

class CalcInAmtGivenOutRequest(_message.Message):
    __slots__ = ['calc_in_amt_given_out']
    CALC_IN_AMT_GIVEN_OUT_FIELD_NUMBER: _ClassVar[int]
    calc_in_amt_given_out: CalcInAmtGivenOut

    def __init__(self, calc_in_amt_given_out: _Optional[_Union[CalcInAmtGivenOut, _Mapping]]=...) -> None:
        ...

class CalcInAmtGivenOutResponse(_message.Message):
    __slots__ = ['token_in']
    TOKEN_IN_FIELD_NUMBER: _ClassVar[int]
    token_in: _coin_pb2.Coin

    def __init__(self, token_in: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=...) -> None:
        ...