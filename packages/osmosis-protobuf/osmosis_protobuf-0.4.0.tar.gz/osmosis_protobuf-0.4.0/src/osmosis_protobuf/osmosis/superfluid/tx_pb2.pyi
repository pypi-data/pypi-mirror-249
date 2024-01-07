from gogoproto import gogo_pb2 as _gogo_pb2
from amino import amino_pb2 as _amino_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from osmosis.superfluid import superfluid_pb2 as _superfluid_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class MsgSuperfluidDelegate(_message.Message):
    __slots__ = ['sender', 'lock_id', 'val_addr']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    LOCK_ID_FIELD_NUMBER: _ClassVar[int]
    VAL_ADDR_FIELD_NUMBER: _ClassVar[int]
    sender: str
    lock_id: int
    val_addr: str

    def __init__(self, sender: _Optional[str]=..., lock_id: _Optional[int]=..., val_addr: _Optional[str]=...) -> None:
        ...

class MsgSuperfluidDelegateResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgSuperfluidUndelegate(_message.Message):
    __slots__ = ['sender', 'lock_id']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    LOCK_ID_FIELD_NUMBER: _ClassVar[int]
    sender: str
    lock_id: int

    def __init__(self, sender: _Optional[str]=..., lock_id: _Optional[int]=...) -> None:
        ...

class MsgSuperfluidUndelegateResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgSuperfluidUnbondLock(_message.Message):
    __slots__ = ['sender', 'lock_id']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    LOCK_ID_FIELD_NUMBER: _ClassVar[int]
    sender: str
    lock_id: int

    def __init__(self, sender: _Optional[str]=..., lock_id: _Optional[int]=...) -> None:
        ...

class MsgSuperfluidUnbondLockResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgSuperfluidUndelegateAndUnbondLock(_message.Message):
    __slots__ = ['sender', 'lock_id', 'coin']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    LOCK_ID_FIELD_NUMBER: _ClassVar[int]
    COIN_FIELD_NUMBER: _ClassVar[int]
    sender: str
    lock_id: int
    coin: _coin_pb2.Coin

    def __init__(self, sender: _Optional[str]=..., lock_id: _Optional[int]=..., coin: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=...) -> None:
        ...

class MsgSuperfluidUndelegateAndUnbondLockResponse(_message.Message):
    __slots__ = ['lock_id']
    LOCK_ID_FIELD_NUMBER: _ClassVar[int]
    lock_id: int

    def __init__(self, lock_id: _Optional[int]=...) -> None:
        ...

class MsgLockAndSuperfluidDelegate(_message.Message):
    __slots__ = ['sender', 'coins', 'val_addr']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    COINS_FIELD_NUMBER: _ClassVar[int]
    VAL_ADDR_FIELD_NUMBER: _ClassVar[int]
    sender: str
    coins: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    val_addr: str

    def __init__(self, sender: _Optional[str]=..., coins: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=..., val_addr: _Optional[str]=...) -> None:
        ...

class MsgLockAndSuperfluidDelegateResponse(_message.Message):
    __slots__ = ['ID']
    ID_FIELD_NUMBER: _ClassVar[int]
    ID: int

    def __init__(self, ID: _Optional[int]=...) -> None:
        ...

class MsgCreateFullRangePositionAndSuperfluidDelegate(_message.Message):
    __slots__ = ['sender', 'coins', 'val_addr', 'pool_id']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    COINS_FIELD_NUMBER: _ClassVar[int]
    VAL_ADDR_FIELD_NUMBER: _ClassVar[int]
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    sender: str
    coins: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    val_addr: str
    pool_id: int

    def __init__(self, sender: _Optional[str]=..., coins: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=..., val_addr: _Optional[str]=..., pool_id: _Optional[int]=...) -> None:
        ...

class MsgCreateFullRangePositionAndSuperfluidDelegateResponse(_message.Message):
    __slots__ = ['lockID', 'positionID']
    LOCKID_FIELD_NUMBER: _ClassVar[int]
    POSITIONID_FIELD_NUMBER: _ClassVar[int]
    lockID: int
    positionID: int

    def __init__(self, lockID: _Optional[int]=..., positionID: _Optional[int]=...) -> None:
        ...

class MsgUnPoolWhitelistedPool(_message.Message):
    __slots__ = ['sender', 'pool_id']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    sender: str
    pool_id: int

    def __init__(self, sender: _Optional[str]=..., pool_id: _Optional[int]=...) -> None:
        ...

class MsgUnPoolWhitelistedPoolResponse(_message.Message):
    __slots__ = ['exited_lock_ids']
    EXITED_LOCK_IDS_FIELD_NUMBER: _ClassVar[int]
    exited_lock_ids: _containers.RepeatedScalarFieldContainer[int]

    def __init__(self, exited_lock_ids: _Optional[_Iterable[int]]=...) -> None:
        ...

class MsgUnlockAndMigrateSharesToFullRangeConcentratedPosition(_message.Message):
    __slots__ = ['sender', 'lock_id', 'shares_to_migrate', 'token_out_mins']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    LOCK_ID_FIELD_NUMBER: _ClassVar[int]
    SHARES_TO_MIGRATE_FIELD_NUMBER: _ClassVar[int]
    TOKEN_OUT_MINS_FIELD_NUMBER: _ClassVar[int]
    sender: str
    lock_id: int
    shares_to_migrate: _coin_pb2.Coin
    token_out_mins: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, sender: _Optional[str]=..., lock_id: _Optional[int]=..., shares_to_migrate: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=..., token_out_mins: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class MsgUnlockAndMigrateSharesToFullRangeConcentratedPositionResponse(_message.Message):
    __slots__ = ['amount0', 'amount1', 'liquidity_created', 'join_time']
    AMOUNT0_FIELD_NUMBER: _ClassVar[int]
    AMOUNT1_FIELD_NUMBER: _ClassVar[int]
    LIQUIDITY_CREATED_FIELD_NUMBER: _ClassVar[int]
    JOIN_TIME_FIELD_NUMBER: _ClassVar[int]
    amount0: str
    amount1: str
    liquidity_created: str
    join_time: _timestamp_pb2.Timestamp

    def __init__(self, amount0: _Optional[str]=..., amount1: _Optional[str]=..., liquidity_created: _Optional[str]=..., join_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
        ...

class MsgAddToConcentratedLiquiditySuperfluidPosition(_message.Message):
    __slots__ = ['position_id', 'sender', 'token_desired0', 'token_desired1']
    POSITION_ID_FIELD_NUMBER: _ClassVar[int]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    TOKEN_DESIRED0_FIELD_NUMBER: _ClassVar[int]
    TOKEN_DESIRED1_FIELD_NUMBER: _ClassVar[int]
    position_id: int
    sender: str
    token_desired0: _coin_pb2.Coin
    token_desired1: _coin_pb2.Coin

    def __init__(self, position_id: _Optional[int]=..., sender: _Optional[str]=..., token_desired0: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=..., token_desired1: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=...) -> None:
        ...

class MsgAddToConcentratedLiquiditySuperfluidPositionResponse(_message.Message):
    __slots__ = ['position_id', 'amount0', 'amount1', 'new_liquidity', 'lock_id']
    POSITION_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT0_FIELD_NUMBER: _ClassVar[int]
    AMOUNT1_FIELD_NUMBER: _ClassVar[int]
    NEW_LIQUIDITY_FIELD_NUMBER: _ClassVar[int]
    LOCK_ID_FIELD_NUMBER: _ClassVar[int]
    position_id: int
    amount0: str
    amount1: str
    new_liquidity: str
    lock_id: int

    def __init__(self, position_id: _Optional[int]=..., amount0: _Optional[str]=..., amount1: _Optional[str]=..., new_liquidity: _Optional[str]=..., lock_id: _Optional[int]=...) -> None:
        ...

class MsgUnbondConvertAndStake(_message.Message):
    __slots__ = ['lock_id', 'sender', 'val_addr', 'min_amt_to_stake', 'shares_to_convert']
    LOCK_ID_FIELD_NUMBER: _ClassVar[int]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    VAL_ADDR_FIELD_NUMBER: _ClassVar[int]
    MIN_AMT_TO_STAKE_FIELD_NUMBER: _ClassVar[int]
    SHARES_TO_CONVERT_FIELD_NUMBER: _ClassVar[int]
    lock_id: int
    sender: str
    val_addr: str
    min_amt_to_stake: str
    shares_to_convert: _coin_pb2.Coin

    def __init__(self, lock_id: _Optional[int]=..., sender: _Optional[str]=..., val_addr: _Optional[str]=..., min_amt_to_stake: _Optional[str]=..., shares_to_convert: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=...) -> None:
        ...

class MsgUnbondConvertAndStakeResponse(_message.Message):
    __slots__ = ['total_amt_staked']
    TOTAL_AMT_STAKED_FIELD_NUMBER: _ClassVar[int]
    total_amt_staked: str

    def __init__(self, total_amt_staked: _Optional[str]=...) -> None:
        ...