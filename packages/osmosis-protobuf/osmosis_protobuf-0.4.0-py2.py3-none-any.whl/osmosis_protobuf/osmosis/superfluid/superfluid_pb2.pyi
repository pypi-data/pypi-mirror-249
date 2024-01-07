from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from osmosis.lockup import lock_pb2 as _lock_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class SuperfluidAssetType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    SuperfluidAssetTypeNative: _ClassVar[SuperfluidAssetType]
    SuperfluidAssetTypeLPShare: _ClassVar[SuperfluidAssetType]
    SuperfluidAssetTypeConcentratedShare: _ClassVar[SuperfluidAssetType]
SuperfluidAssetTypeNative: SuperfluidAssetType
SuperfluidAssetTypeLPShare: SuperfluidAssetType
SuperfluidAssetTypeConcentratedShare: SuperfluidAssetType

class SuperfluidAsset(_message.Message):
    __slots__ = ['denom', 'asset_type']
    DENOM_FIELD_NUMBER: _ClassVar[int]
    ASSET_TYPE_FIELD_NUMBER: _ClassVar[int]
    denom: str
    asset_type: SuperfluidAssetType

    def __init__(self, denom: _Optional[str]=..., asset_type: _Optional[_Union[SuperfluidAssetType, str]]=...) -> None:
        ...

class SuperfluidIntermediaryAccount(_message.Message):
    __slots__ = ['denom', 'val_addr', 'gauge_id']
    DENOM_FIELD_NUMBER: _ClassVar[int]
    VAL_ADDR_FIELD_NUMBER: _ClassVar[int]
    GAUGE_ID_FIELD_NUMBER: _ClassVar[int]
    denom: str
    val_addr: str
    gauge_id: int

    def __init__(self, denom: _Optional[str]=..., val_addr: _Optional[str]=..., gauge_id: _Optional[int]=...) -> None:
        ...

class OsmoEquivalentMultiplierRecord(_message.Message):
    __slots__ = ['epoch_number', 'denom', 'multiplier']
    EPOCH_NUMBER_FIELD_NUMBER: _ClassVar[int]
    DENOM_FIELD_NUMBER: _ClassVar[int]
    MULTIPLIER_FIELD_NUMBER: _ClassVar[int]
    epoch_number: int
    denom: str
    multiplier: str

    def __init__(self, epoch_number: _Optional[int]=..., denom: _Optional[str]=..., multiplier: _Optional[str]=...) -> None:
        ...

class SuperfluidDelegationRecord(_message.Message):
    __slots__ = ['delegator_address', 'validator_address', 'delegation_amount', 'equivalent_staked_amount']
    DELEGATOR_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    VALIDATOR_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    DELEGATION_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    EQUIVALENT_STAKED_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    delegator_address: str
    validator_address: str
    delegation_amount: _coin_pb2.Coin
    equivalent_staked_amount: _coin_pb2.Coin

    def __init__(self, delegator_address: _Optional[str]=..., validator_address: _Optional[str]=..., delegation_amount: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=..., equivalent_staked_amount: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=...) -> None:
        ...

class LockIdIntermediaryAccountConnection(_message.Message):
    __slots__ = ['lock_id', 'intermediary_account']
    LOCK_ID_FIELD_NUMBER: _ClassVar[int]
    INTERMEDIARY_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    lock_id: int
    intermediary_account: str

    def __init__(self, lock_id: _Optional[int]=..., intermediary_account: _Optional[str]=...) -> None:
        ...

class UnpoolWhitelistedPools(_message.Message):
    __slots__ = ['ids']
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[int]

    def __init__(self, ids: _Optional[_Iterable[int]]=...) -> None:
        ...

class ConcentratedPoolUserPositionRecord(_message.Message):
    __slots__ = ['validator_address', 'position_id', 'lock_id', 'synthetic_lock', 'delegation_amount', 'equivalent_staked_amount']
    VALIDATOR_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    POSITION_ID_FIELD_NUMBER: _ClassVar[int]
    LOCK_ID_FIELD_NUMBER: _ClassVar[int]
    SYNTHETIC_LOCK_FIELD_NUMBER: _ClassVar[int]
    DELEGATION_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    EQUIVALENT_STAKED_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    validator_address: str
    position_id: int
    lock_id: int
    synthetic_lock: _lock_pb2.SyntheticLock
    delegation_amount: _coin_pb2.Coin
    equivalent_staked_amount: _coin_pb2.Coin

    def __init__(self, validator_address: _Optional[str]=..., position_id: _Optional[int]=..., lock_id: _Optional[int]=..., synthetic_lock: _Optional[_Union[_lock_pb2.SyntheticLock, _Mapping]]=..., delegation_amount: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=..., equivalent_staked_amount: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=...) -> None:
        ...