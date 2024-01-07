from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from osmosis.superfluid import superfluid_pb2 as _superfluid_pb2
from osmosis.superfluid import params_pb2 as _params_pb2
from osmosis.lockup import lock_pb2 as _lock_pb2
from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from cosmos.staking.v1beta1 import staking_pb2 as _staking_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

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

class AssetTypeRequest(_message.Message):
    __slots__ = ['denom']
    DENOM_FIELD_NUMBER: _ClassVar[int]
    denom: str

    def __init__(self, denom: _Optional[str]=...) -> None:
        ...

class AssetTypeResponse(_message.Message):
    __slots__ = ['asset_type']
    ASSET_TYPE_FIELD_NUMBER: _ClassVar[int]
    asset_type: _superfluid_pb2.SuperfluidAssetType

    def __init__(self, asset_type: _Optional[_Union[_superfluid_pb2.SuperfluidAssetType, str]]=...) -> None:
        ...

class AllAssetsRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class AllAssetsResponse(_message.Message):
    __slots__ = ['assets']
    ASSETS_FIELD_NUMBER: _ClassVar[int]
    assets: _containers.RepeatedCompositeFieldContainer[_superfluid_pb2.SuperfluidAsset]

    def __init__(self, assets: _Optional[_Iterable[_Union[_superfluid_pb2.SuperfluidAsset, _Mapping]]]=...) -> None:
        ...

class AssetMultiplierRequest(_message.Message):
    __slots__ = ['denom']
    DENOM_FIELD_NUMBER: _ClassVar[int]
    denom: str

    def __init__(self, denom: _Optional[str]=...) -> None:
        ...

class AssetMultiplierResponse(_message.Message):
    __slots__ = ['osmo_equivalent_multiplier']
    OSMO_EQUIVALENT_MULTIPLIER_FIELD_NUMBER: _ClassVar[int]
    osmo_equivalent_multiplier: _superfluid_pb2.OsmoEquivalentMultiplierRecord

    def __init__(self, osmo_equivalent_multiplier: _Optional[_Union[_superfluid_pb2.OsmoEquivalentMultiplierRecord, _Mapping]]=...) -> None:
        ...

class SuperfluidIntermediaryAccountInfo(_message.Message):
    __slots__ = ['denom', 'val_addr', 'gauge_id', 'address']
    DENOM_FIELD_NUMBER: _ClassVar[int]
    VAL_ADDR_FIELD_NUMBER: _ClassVar[int]
    GAUGE_ID_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    denom: str
    val_addr: str
    gauge_id: int
    address: str

    def __init__(self, denom: _Optional[str]=..., val_addr: _Optional[str]=..., gauge_id: _Optional[int]=..., address: _Optional[str]=...) -> None:
        ...

class AllIntermediaryAccountsRequest(_message.Message):
    __slots__ = ['pagination']
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageRequest

    def __init__(self, pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]]=...) -> None:
        ...

class AllIntermediaryAccountsResponse(_message.Message):
    __slots__ = ['accounts', 'pagination']
    ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    accounts: _containers.RepeatedCompositeFieldContainer[SuperfluidIntermediaryAccountInfo]
    pagination: _pagination_pb2.PageResponse

    def __init__(self, accounts: _Optional[_Iterable[_Union[SuperfluidIntermediaryAccountInfo, _Mapping]]]=..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]]=...) -> None:
        ...

class ConnectedIntermediaryAccountRequest(_message.Message):
    __slots__ = ['lock_id']
    LOCK_ID_FIELD_NUMBER: _ClassVar[int]
    lock_id: int

    def __init__(self, lock_id: _Optional[int]=...) -> None:
        ...

class ConnectedIntermediaryAccountResponse(_message.Message):
    __slots__ = ['account']
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    account: SuperfluidIntermediaryAccountInfo

    def __init__(self, account: _Optional[_Union[SuperfluidIntermediaryAccountInfo, _Mapping]]=...) -> None:
        ...

class QueryTotalDelegationByValidatorForDenomRequest(_message.Message):
    __slots__ = ['denom']
    DENOM_FIELD_NUMBER: _ClassVar[int]
    denom: str

    def __init__(self, denom: _Optional[str]=...) -> None:
        ...

class QueryTotalDelegationByValidatorForDenomResponse(_message.Message):
    __slots__ = ['assets']
    ASSETS_FIELD_NUMBER: _ClassVar[int]
    assets: _containers.RepeatedCompositeFieldContainer[Delegations]

    def __init__(self, assets: _Optional[_Iterable[_Union[Delegations, _Mapping]]]=...) -> None:
        ...

class Delegations(_message.Message):
    __slots__ = ['val_addr', 'amount_sfsd', 'osmo_equivalent']
    VAL_ADDR_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_SFSD_FIELD_NUMBER: _ClassVar[int]
    OSMO_EQUIVALENT_FIELD_NUMBER: _ClassVar[int]
    val_addr: str
    amount_sfsd: str
    osmo_equivalent: str

    def __init__(self, val_addr: _Optional[str]=..., amount_sfsd: _Optional[str]=..., osmo_equivalent: _Optional[str]=...) -> None:
        ...

class TotalSuperfluidDelegationsRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class TotalSuperfluidDelegationsResponse(_message.Message):
    __slots__ = ['total_delegations']
    TOTAL_DELEGATIONS_FIELD_NUMBER: _ClassVar[int]
    total_delegations: str

    def __init__(self, total_delegations: _Optional[str]=...) -> None:
        ...

class SuperfluidDelegationAmountRequest(_message.Message):
    __slots__ = ['delegator_address', 'validator_address', 'denom']
    DELEGATOR_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    VALIDATOR_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    DENOM_FIELD_NUMBER: _ClassVar[int]
    delegator_address: str
    validator_address: str
    denom: str

    def __init__(self, delegator_address: _Optional[str]=..., validator_address: _Optional[str]=..., denom: _Optional[str]=...) -> None:
        ...

class SuperfluidDelegationAmountResponse(_message.Message):
    __slots__ = ['amount']
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    amount: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, amount: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class SuperfluidDelegationsByDelegatorRequest(_message.Message):
    __slots__ = ['delegator_address']
    DELEGATOR_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    delegator_address: str

    def __init__(self, delegator_address: _Optional[str]=...) -> None:
        ...

class SuperfluidDelegationsByDelegatorResponse(_message.Message):
    __slots__ = ['superfluid_delegation_records', 'total_delegated_coins', 'total_equivalent_staked_amount']
    SUPERFLUID_DELEGATION_RECORDS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_DELEGATED_COINS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_EQUIVALENT_STAKED_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    superfluid_delegation_records: _containers.RepeatedCompositeFieldContainer[_superfluid_pb2.SuperfluidDelegationRecord]
    total_delegated_coins: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    total_equivalent_staked_amount: _coin_pb2.Coin

    def __init__(self, superfluid_delegation_records: _Optional[_Iterable[_Union[_superfluid_pb2.SuperfluidDelegationRecord, _Mapping]]]=..., total_delegated_coins: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=..., total_equivalent_staked_amount: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=...) -> None:
        ...

class SuperfluidUndelegationsByDelegatorRequest(_message.Message):
    __slots__ = ['delegator_address', 'denom']
    DELEGATOR_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    DENOM_FIELD_NUMBER: _ClassVar[int]
    delegator_address: str
    denom: str

    def __init__(self, delegator_address: _Optional[str]=..., denom: _Optional[str]=...) -> None:
        ...

class SuperfluidUndelegationsByDelegatorResponse(_message.Message):
    __slots__ = ['superfluid_delegation_records', 'total_undelegated_coins', 'synthetic_locks']
    SUPERFLUID_DELEGATION_RECORDS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_UNDELEGATED_COINS_FIELD_NUMBER: _ClassVar[int]
    SYNTHETIC_LOCKS_FIELD_NUMBER: _ClassVar[int]
    superfluid_delegation_records: _containers.RepeatedCompositeFieldContainer[_superfluid_pb2.SuperfluidDelegationRecord]
    total_undelegated_coins: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    synthetic_locks: _containers.RepeatedCompositeFieldContainer[_lock_pb2.SyntheticLock]

    def __init__(self, superfluid_delegation_records: _Optional[_Iterable[_Union[_superfluid_pb2.SuperfluidDelegationRecord, _Mapping]]]=..., total_undelegated_coins: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=..., synthetic_locks: _Optional[_Iterable[_Union[_lock_pb2.SyntheticLock, _Mapping]]]=...) -> None:
        ...

class SuperfluidDelegationsByValidatorDenomRequest(_message.Message):
    __slots__ = ['validator_address', 'denom']
    VALIDATOR_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    DENOM_FIELD_NUMBER: _ClassVar[int]
    validator_address: str
    denom: str

    def __init__(self, validator_address: _Optional[str]=..., denom: _Optional[str]=...) -> None:
        ...

class SuperfluidDelegationsByValidatorDenomResponse(_message.Message):
    __slots__ = ['superfluid_delegation_records']
    SUPERFLUID_DELEGATION_RECORDS_FIELD_NUMBER: _ClassVar[int]
    superfluid_delegation_records: _containers.RepeatedCompositeFieldContainer[_superfluid_pb2.SuperfluidDelegationRecord]

    def __init__(self, superfluid_delegation_records: _Optional[_Iterable[_Union[_superfluid_pb2.SuperfluidDelegationRecord, _Mapping]]]=...) -> None:
        ...

class EstimateSuperfluidDelegatedAmountByValidatorDenomRequest(_message.Message):
    __slots__ = ['validator_address', 'denom']
    VALIDATOR_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    DENOM_FIELD_NUMBER: _ClassVar[int]
    validator_address: str
    denom: str

    def __init__(self, validator_address: _Optional[str]=..., denom: _Optional[str]=...) -> None:
        ...

class EstimateSuperfluidDelegatedAmountByValidatorDenomResponse(_message.Message):
    __slots__ = ['total_delegated_coins']
    TOTAL_DELEGATED_COINS_FIELD_NUMBER: _ClassVar[int]
    total_delegated_coins: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, total_delegated_coins: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class QueryTotalDelegationByDelegatorRequest(_message.Message):
    __slots__ = ['delegator_address']
    DELEGATOR_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    delegator_address: str

    def __init__(self, delegator_address: _Optional[str]=...) -> None:
        ...

class QueryTotalDelegationByDelegatorResponse(_message.Message):
    __slots__ = ['superfluid_delegation_records', 'delegation_response', 'total_delegated_coins', 'total_equivalent_staked_amount']
    SUPERFLUID_DELEGATION_RECORDS_FIELD_NUMBER: _ClassVar[int]
    DELEGATION_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_DELEGATED_COINS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_EQUIVALENT_STAKED_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    superfluid_delegation_records: _containers.RepeatedCompositeFieldContainer[_superfluid_pb2.SuperfluidDelegationRecord]
    delegation_response: _containers.RepeatedCompositeFieldContainer[_staking_pb2.DelegationResponse]
    total_delegated_coins: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    total_equivalent_staked_amount: _coin_pb2.Coin

    def __init__(self, superfluid_delegation_records: _Optional[_Iterable[_Union[_superfluid_pb2.SuperfluidDelegationRecord, _Mapping]]]=..., delegation_response: _Optional[_Iterable[_Union[_staking_pb2.DelegationResponse, _Mapping]]]=..., total_delegated_coins: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=..., total_equivalent_staked_amount: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=...) -> None:
        ...

class QueryUnpoolWhitelistRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryUnpoolWhitelistResponse(_message.Message):
    __slots__ = ['pool_ids']
    POOL_IDS_FIELD_NUMBER: _ClassVar[int]
    pool_ids: _containers.RepeatedScalarFieldContainer[int]

    def __init__(self, pool_ids: _Optional[_Iterable[int]]=...) -> None:
        ...

class UserConcentratedSuperfluidPositionsDelegatedRequest(_message.Message):
    __slots__ = ['delegator_address']
    DELEGATOR_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    delegator_address: str

    def __init__(self, delegator_address: _Optional[str]=...) -> None:
        ...

class UserConcentratedSuperfluidPositionsDelegatedResponse(_message.Message):
    __slots__ = ['cl_pool_user_position_records']
    CL_POOL_USER_POSITION_RECORDS_FIELD_NUMBER: _ClassVar[int]
    cl_pool_user_position_records: _containers.RepeatedCompositeFieldContainer[_superfluid_pb2.ConcentratedPoolUserPositionRecord]

    def __init__(self, cl_pool_user_position_records: _Optional[_Iterable[_Union[_superfluid_pb2.ConcentratedPoolUserPositionRecord, _Mapping]]]=...) -> None:
        ...

class UserConcentratedSuperfluidPositionsUndelegatingRequest(_message.Message):
    __slots__ = ['delegator_address']
    DELEGATOR_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    delegator_address: str

    def __init__(self, delegator_address: _Optional[str]=...) -> None:
        ...

class UserConcentratedSuperfluidPositionsUndelegatingResponse(_message.Message):
    __slots__ = ['cl_pool_user_position_records']
    CL_POOL_USER_POSITION_RECORDS_FIELD_NUMBER: _ClassVar[int]
    cl_pool_user_position_records: _containers.RepeatedCompositeFieldContainer[_superfluid_pb2.ConcentratedPoolUserPositionRecord]

    def __init__(self, cl_pool_user_position_records: _Optional[_Iterable[_Union[_superfluid_pb2.ConcentratedPoolUserPositionRecord, _Mapping]]]=...) -> None:
        ...

class QueryRestSupplyRequest(_message.Message):
    __slots__ = ['denom']
    DENOM_FIELD_NUMBER: _ClassVar[int]
    denom: str

    def __init__(self, denom: _Optional[str]=...) -> None:
        ...

class QueryRestSupplyResponse(_message.Message):
    __slots__ = ['amount']
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    amount: _coin_pb2.Coin

    def __init__(self, amount: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=...) -> None:
        ...