from gogoproto import gogo_pb2 as _gogo_pb2
from osmosis.superfluid import superfluid_pb2 as _superfluid_pb2
from osmosis.superfluid import params_pb2 as _params_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class GenesisState(_message.Message):
    __slots__ = ['params', 'superfluid_assets', 'osmo_equivalent_multipliers', 'intermediary_accounts', 'intemediary_account_connections']
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    SUPERFLUID_ASSETS_FIELD_NUMBER: _ClassVar[int]
    OSMO_EQUIVALENT_MULTIPLIERS_FIELD_NUMBER: _ClassVar[int]
    INTERMEDIARY_ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    INTEMEDIARY_ACCOUNT_CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    params: _params_pb2.Params
    superfluid_assets: _containers.RepeatedCompositeFieldContainer[_superfluid_pb2.SuperfluidAsset]
    osmo_equivalent_multipliers: _containers.RepeatedCompositeFieldContainer[_superfluid_pb2.OsmoEquivalentMultiplierRecord]
    intermediary_accounts: _containers.RepeatedCompositeFieldContainer[_superfluid_pb2.SuperfluidIntermediaryAccount]
    intemediary_account_connections: _containers.RepeatedCompositeFieldContainer[_superfluid_pb2.LockIdIntermediaryAccountConnection]

    def __init__(self, params: _Optional[_Union[_params_pb2.Params, _Mapping]]=..., superfluid_assets: _Optional[_Iterable[_Union[_superfluid_pb2.SuperfluidAsset, _Mapping]]]=..., osmo_equivalent_multipliers: _Optional[_Iterable[_Union[_superfluid_pb2.OsmoEquivalentMultiplierRecord, _Mapping]]]=..., intermediary_accounts: _Optional[_Iterable[_Union[_superfluid_pb2.SuperfluidIntermediaryAccount, _Mapping]]]=..., intemediary_account_connections: _Optional[_Iterable[_Union[_superfluid_pb2.LockIdIntermediaryAccountConnection, _Mapping]]]=...) -> None:
        ...