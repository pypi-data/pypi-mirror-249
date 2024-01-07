from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from osmosis.lockup import lock_pb2 as _lock_pb2
from osmosis.lockup import params_pb2 as _params_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class ModuleBalanceRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class ModuleBalanceResponse(_message.Message):
    __slots__ = ['coins']
    COINS_FIELD_NUMBER: _ClassVar[int]
    coins: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, coins: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class ModuleLockedAmountRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class ModuleLockedAmountResponse(_message.Message):
    __slots__ = ['coins']
    COINS_FIELD_NUMBER: _ClassVar[int]
    coins: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, coins: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class AccountUnlockableCoinsRequest(_message.Message):
    __slots__ = ['owner']
    OWNER_FIELD_NUMBER: _ClassVar[int]
    owner: str

    def __init__(self, owner: _Optional[str]=...) -> None:
        ...

class AccountUnlockableCoinsResponse(_message.Message):
    __slots__ = ['coins']
    COINS_FIELD_NUMBER: _ClassVar[int]
    coins: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, coins: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class AccountUnlockingCoinsRequest(_message.Message):
    __slots__ = ['owner']
    OWNER_FIELD_NUMBER: _ClassVar[int]
    owner: str

    def __init__(self, owner: _Optional[str]=...) -> None:
        ...

class AccountUnlockingCoinsResponse(_message.Message):
    __slots__ = ['coins']
    COINS_FIELD_NUMBER: _ClassVar[int]
    coins: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, coins: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class AccountLockedCoinsRequest(_message.Message):
    __slots__ = ['owner']
    OWNER_FIELD_NUMBER: _ClassVar[int]
    owner: str

    def __init__(self, owner: _Optional[str]=...) -> None:
        ...

class AccountLockedCoinsResponse(_message.Message):
    __slots__ = ['coins']
    COINS_FIELD_NUMBER: _ClassVar[int]
    coins: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, coins: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class AccountLockedPastTimeRequest(_message.Message):
    __slots__ = ['owner', 'timestamp']
    OWNER_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    owner: str
    timestamp: _timestamp_pb2.Timestamp

    def __init__(self, owner: _Optional[str]=..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
        ...

class AccountLockedPastTimeResponse(_message.Message):
    __slots__ = ['locks']
    LOCKS_FIELD_NUMBER: _ClassVar[int]
    locks: _containers.RepeatedCompositeFieldContainer[_lock_pb2.PeriodLock]

    def __init__(self, locks: _Optional[_Iterable[_Union[_lock_pb2.PeriodLock, _Mapping]]]=...) -> None:
        ...

class AccountLockedPastTimeNotUnlockingOnlyRequest(_message.Message):
    __slots__ = ['owner', 'timestamp']
    OWNER_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    owner: str
    timestamp: _timestamp_pb2.Timestamp

    def __init__(self, owner: _Optional[str]=..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
        ...

class AccountLockedPastTimeNotUnlockingOnlyResponse(_message.Message):
    __slots__ = ['locks']
    LOCKS_FIELD_NUMBER: _ClassVar[int]
    locks: _containers.RepeatedCompositeFieldContainer[_lock_pb2.PeriodLock]

    def __init__(self, locks: _Optional[_Iterable[_Union[_lock_pb2.PeriodLock, _Mapping]]]=...) -> None:
        ...

class AccountUnlockedBeforeTimeRequest(_message.Message):
    __slots__ = ['owner', 'timestamp']
    OWNER_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    owner: str
    timestamp: _timestamp_pb2.Timestamp

    def __init__(self, owner: _Optional[str]=..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
        ...

class AccountUnlockedBeforeTimeResponse(_message.Message):
    __slots__ = ['locks']
    LOCKS_FIELD_NUMBER: _ClassVar[int]
    locks: _containers.RepeatedCompositeFieldContainer[_lock_pb2.PeriodLock]

    def __init__(self, locks: _Optional[_Iterable[_Union[_lock_pb2.PeriodLock, _Mapping]]]=...) -> None:
        ...

class AccountLockedPastTimeDenomRequest(_message.Message):
    __slots__ = ['owner', 'timestamp', 'denom']
    OWNER_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DENOM_FIELD_NUMBER: _ClassVar[int]
    owner: str
    timestamp: _timestamp_pb2.Timestamp
    denom: str

    def __init__(self, owner: _Optional[str]=..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., denom: _Optional[str]=...) -> None:
        ...

class AccountLockedPastTimeDenomResponse(_message.Message):
    __slots__ = ['locks']
    LOCKS_FIELD_NUMBER: _ClassVar[int]
    locks: _containers.RepeatedCompositeFieldContainer[_lock_pb2.PeriodLock]

    def __init__(self, locks: _Optional[_Iterable[_Union[_lock_pb2.PeriodLock, _Mapping]]]=...) -> None:
        ...

class LockedDenomRequest(_message.Message):
    __slots__ = ['denom', 'duration']
    DENOM_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    denom: str
    duration: _duration_pb2.Duration

    def __init__(self, denom: _Optional[str]=..., duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]]=...) -> None:
        ...

class LockedDenomResponse(_message.Message):
    __slots__ = ['amount']
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    amount: str

    def __init__(self, amount: _Optional[str]=...) -> None:
        ...

class LockedRequest(_message.Message):
    __slots__ = ['lock_id']
    LOCK_ID_FIELD_NUMBER: _ClassVar[int]
    lock_id: int

    def __init__(self, lock_id: _Optional[int]=...) -> None:
        ...

class LockedResponse(_message.Message):
    __slots__ = ['lock']
    LOCK_FIELD_NUMBER: _ClassVar[int]
    lock: _lock_pb2.PeriodLock

    def __init__(self, lock: _Optional[_Union[_lock_pb2.PeriodLock, _Mapping]]=...) -> None:
        ...

class LockRewardReceiverRequest(_message.Message):
    __slots__ = ['lock_id']
    LOCK_ID_FIELD_NUMBER: _ClassVar[int]
    lock_id: int

    def __init__(self, lock_id: _Optional[int]=...) -> None:
        ...

class LockRewardReceiverResponse(_message.Message):
    __slots__ = ['reward_receiver']
    REWARD_RECEIVER_FIELD_NUMBER: _ClassVar[int]
    reward_receiver: str

    def __init__(self, reward_receiver: _Optional[str]=...) -> None:
        ...

class NextLockIDRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class NextLockIDResponse(_message.Message):
    __slots__ = ['lock_id']
    LOCK_ID_FIELD_NUMBER: _ClassVar[int]
    lock_id: int

    def __init__(self, lock_id: _Optional[int]=...) -> None:
        ...

class SyntheticLockupsByLockupIDRequest(_message.Message):
    __slots__ = ['lock_id']
    LOCK_ID_FIELD_NUMBER: _ClassVar[int]
    lock_id: int

    def __init__(self, lock_id: _Optional[int]=...) -> None:
        ...

class SyntheticLockupsByLockupIDResponse(_message.Message):
    __slots__ = ['synthetic_locks']
    SYNTHETIC_LOCKS_FIELD_NUMBER: _ClassVar[int]
    synthetic_locks: _containers.RepeatedCompositeFieldContainer[_lock_pb2.SyntheticLock]

    def __init__(self, synthetic_locks: _Optional[_Iterable[_Union[_lock_pb2.SyntheticLock, _Mapping]]]=...) -> None:
        ...

class SyntheticLockupByLockupIDRequest(_message.Message):
    __slots__ = ['lock_id']
    LOCK_ID_FIELD_NUMBER: _ClassVar[int]
    lock_id: int

    def __init__(self, lock_id: _Optional[int]=...) -> None:
        ...

class SyntheticLockupByLockupIDResponse(_message.Message):
    __slots__ = ['synthetic_lock']
    SYNTHETIC_LOCK_FIELD_NUMBER: _ClassVar[int]
    synthetic_lock: _lock_pb2.SyntheticLock

    def __init__(self, synthetic_lock: _Optional[_Union[_lock_pb2.SyntheticLock, _Mapping]]=...) -> None:
        ...

class AccountLockedLongerDurationRequest(_message.Message):
    __slots__ = ['owner', 'duration']
    OWNER_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    owner: str
    duration: _duration_pb2.Duration

    def __init__(self, owner: _Optional[str]=..., duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]]=...) -> None:
        ...

class AccountLockedLongerDurationResponse(_message.Message):
    __slots__ = ['locks']
    LOCKS_FIELD_NUMBER: _ClassVar[int]
    locks: _containers.RepeatedCompositeFieldContainer[_lock_pb2.PeriodLock]

    def __init__(self, locks: _Optional[_Iterable[_Union[_lock_pb2.PeriodLock, _Mapping]]]=...) -> None:
        ...

class AccountLockedDurationRequest(_message.Message):
    __slots__ = ['owner', 'duration']
    OWNER_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    owner: str
    duration: _duration_pb2.Duration

    def __init__(self, owner: _Optional[str]=..., duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]]=...) -> None:
        ...

class AccountLockedDurationResponse(_message.Message):
    __slots__ = ['locks']
    LOCKS_FIELD_NUMBER: _ClassVar[int]
    locks: _containers.RepeatedCompositeFieldContainer[_lock_pb2.PeriodLock]

    def __init__(self, locks: _Optional[_Iterable[_Union[_lock_pb2.PeriodLock, _Mapping]]]=...) -> None:
        ...

class AccountLockedLongerDurationNotUnlockingOnlyRequest(_message.Message):
    __slots__ = ['owner', 'duration']
    OWNER_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    owner: str
    duration: _duration_pb2.Duration

    def __init__(self, owner: _Optional[str]=..., duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]]=...) -> None:
        ...

class AccountLockedLongerDurationNotUnlockingOnlyResponse(_message.Message):
    __slots__ = ['locks']
    LOCKS_FIELD_NUMBER: _ClassVar[int]
    locks: _containers.RepeatedCompositeFieldContainer[_lock_pb2.PeriodLock]

    def __init__(self, locks: _Optional[_Iterable[_Union[_lock_pb2.PeriodLock, _Mapping]]]=...) -> None:
        ...

class AccountLockedLongerDurationDenomRequest(_message.Message):
    __slots__ = ['owner', 'duration', 'denom']
    OWNER_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    DENOM_FIELD_NUMBER: _ClassVar[int]
    owner: str
    duration: _duration_pb2.Duration
    denom: str

    def __init__(self, owner: _Optional[str]=..., duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]]=..., denom: _Optional[str]=...) -> None:
        ...

class AccountLockedLongerDurationDenomResponse(_message.Message):
    __slots__ = ['locks']
    LOCKS_FIELD_NUMBER: _ClassVar[int]
    locks: _containers.RepeatedCompositeFieldContainer[_lock_pb2.PeriodLock]

    def __init__(self, locks: _Optional[_Iterable[_Union[_lock_pb2.PeriodLock, _Mapping]]]=...) -> None:
        ...

class QueryParamsRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryParamsResponse(_message.Message):
    __slots__ = ['params']
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: _params_pb2.Params

    def __init__(self, params: _Optional[_Union[_params_pb2.Params, _Mapping]]=...) -> None:
        ...