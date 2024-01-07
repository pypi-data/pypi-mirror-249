"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....amino import amino_pb2 as amino_dot_amino__pb2
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from ....cosmos.auth.v1beta1 import auth_pb2 as cosmos_dot_auth_dot_v1beta1_dot_auth__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$cosmos/vesting/v1beta1/vesting.proto\x12\x16cosmos.vesting.v1beta1\x1a\x11amino/amino.proto\x1a\x14gogoproto/gogo.proto\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a\x1ecosmos/auth/v1beta1/auth.proto"\xd3\x03\n\x12BaseVestingAccount\x12<\n\x0cbase_account\x18\x01 \x01(\x0b2 .cosmos.auth.v1beta1.BaseAccountB\x04\xd0\xde\x1f\x01\x12j\n\x10original_vesting\x18\x02 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB5\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xa8\xe7\xb0*\x01\x12h\n\x0edelegated_free\x18\x03 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB5\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xa8\xe7\xb0*\x01\x12k\n\x11delegated_vesting\x18\x04 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB5\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xa8\xe7\xb0*\x01\x12\x10\n\x08end_time\x18\x05 \x01(\x03:*\x88\xa0\x1f\x00\x98\xa0\x1f\x00\x8a\xe7\xb0*\x1dcosmos-sdk/BaseVestingAccount"\xb0\x01\n\x18ContinuousVestingAccount\x12N\n\x14base_vesting_account\x18\x01 \x01(\x0b2*.cosmos.vesting.v1beta1.BaseVestingAccountB\x04\xd0\xde\x1f\x01\x12\x12\n\nstart_time\x18\x02 \x01(\x03:0\x88\xa0\x1f\x00\x98\xa0\x1f\x00\x8a\xe7\xb0*#cosmos-sdk/ContinuousVestingAccount"\x96\x01\n\x15DelayedVestingAccount\x12N\n\x14base_vesting_account\x18\x01 \x01(\x0b2*.cosmos.vesting.v1beta1.BaseVestingAccountB\x04\xd0\xde\x1f\x01:-\x88\xa0\x1f\x00\x98\xa0\x1f\x00\x8a\xe7\xb0* cosmos-sdk/DelayedVestingAccount"\x80\x01\n\x06Period\x12\x0e\n\x06length\x18\x01 \x01(\x03\x12`\n\x06amount\x18\x02 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB5\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xa8\xe7\xb0*\x01:\x04\x98\xa0\x1f\x00"\xf0\x01\n\x16PeriodicVestingAccount\x12N\n\x14base_vesting_account\x18\x01 \x01(\x0b2*.cosmos.vesting.v1beta1.BaseVestingAccountB\x04\xd0\xde\x1f\x01\x12\x12\n\nstart_time\x18\x02 \x01(\x03\x12B\n\x0fvesting_periods\x18\x03 \x03(\x0b2\x1e.cosmos.vesting.v1beta1.PeriodB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01:.\x88\xa0\x1f\x00\x98\xa0\x1f\x00\x8a\xe7\xb0*!cosmos-sdk/PeriodicVestingAccount"\x98\x01\n\x16PermanentLockedAccount\x12N\n\x14base_vesting_account\x18\x01 \x01(\x0b2*.cosmos.vesting.v1beta1.BaseVestingAccountB\x04\xd0\xde\x1f\x01:.\x88\xa0\x1f\x00\x98\xa0\x1f\x00\x8a\xe7\xb0*!cosmos-sdk/PermanentLockedAccount"\x80\x03\n\x16ClawbackVestingAccount\x12N\n\x14base_vesting_account\x18\x01 \x01(\x0b2*.cosmos.vesting.v1beta1.BaseVestingAccountB\x04\xd0\xde\x1f\x01\x121\n\x0efunder_address\x18\x02 \x01(\tB\x19\xf2\xde\x1f\x15yaml:"funder_address"\x12)\n\nstart_time\x18\x03 \x01(\x03B\x15\xf2\xde\x1f\x11yaml:"start_time"\x12U\n\x0elockup_periods\x18\x04 \x03(\x0b2\x1e.cosmos.vesting.v1beta1.PeriodB\x1d\xc8\xde\x1f\x00\xf2\xde\x1f\x15yaml:"lockup_periods"\x12W\n\x0fvesting_periods\x18\x05 \x03(\x0b2\x1e.cosmos.vesting.v1beta1.PeriodB\x1e\xc8\xde\x1f\x00\xf2\xde\x1f\x16yaml:"vesting_periods":\x08\x88\xa0\x1f\x00\x98\xa0\x1f\x00B3Z1github.com/cosmos/cosmos-sdk/x/auth/vesting/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.vesting.v1beta1.vesting_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z1github.com/cosmos/cosmos-sdk/x/auth/vesting/types'
    _BASEVESTINGACCOUNT.fields_by_name['base_account']._options = None
    _BASEVESTINGACCOUNT.fields_by_name['base_account']._serialized_options = b'\xd0\xde\x1f\x01'
    _BASEVESTINGACCOUNT.fields_by_name['original_vesting']._options = None
    _BASEVESTINGACCOUNT.fields_by_name['original_vesting']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xa8\xe7\xb0*\x01'
    _BASEVESTINGACCOUNT.fields_by_name['delegated_free']._options = None
    _BASEVESTINGACCOUNT.fields_by_name['delegated_free']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xa8\xe7\xb0*\x01'
    _BASEVESTINGACCOUNT.fields_by_name['delegated_vesting']._options = None
    _BASEVESTINGACCOUNT.fields_by_name['delegated_vesting']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xa8\xe7\xb0*\x01'
    _BASEVESTINGACCOUNT._options = None
    _BASEVESTINGACCOUNT._serialized_options = b'\x88\xa0\x1f\x00\x98\xa0\x1f\x00\x8a\xe7\xb0*\x1dcosmos-sdk/BaseVestingAccount'
    _CONTINUOUSVESTINGACCOUNT.fields_by_name['base_vesting_account']._options = None
    _CONTINUOUSVESTINGACCOUNT.fields_by_name['base_vesting_account']._serialized_options = b'\xd0\xde\x1f\x01'
    _CONTINUOUSVESTINGACCOUNT._options = None
    _CONTINUOUSVESTINGACCOUNT._serialized_options = b'\x88\xa0\x1f\x00\x98\xa0\x1f\x00\x8a\xe7\xb0*#cosmos-sdk/ContinuousVestingAccount'
    _DELAYEDVESTINGACCOUNT.fields_by_name['base_vesting_account']._options = None
    _DELAYEDVESTINGACCOUNT.fields_by_name['base_vesting_account']._serialized_options = b'\xd0\xde\x1f\x01'
    _DELAYEDVESTINGACCOUNT._options = None
    _DELAYEDVESTINGACCOUNT._serialized_options = b'\x88\xa0\x1f\x00\x98\xa0\x1f\x00\x8a\xe7\xb0* cosmos-sdk/DelayedVestingAccount'
    _PERIOD.fields_by_name['amount']._options = None
    _PERIOD.fields_by_name['amount']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xa8\xe7\xb0*\x01'
    _PERIOD._options = None
    _PERIOD._serialized_options = b'\x98\xa0\x1f\x00'
    _PERIODICVESTINGACCOUNT.fields_by_name['base_vesting_account']._options = None
    _PERIODICVESTINGACCOUNT.fields_by_name['base_vesting_account']._serialized_options = b'\xd0\xde\x1f\x01'
    _PERIODICVESTINGACCOUNT.fields_by_name['vesting_periods']._options = None
    _PERIODICVESTINGACCOUNT.fields_by_name['vesting_periods']._serialized_options = b'\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01'
    _PERIODICVESTINGACCOUNT._options = None
    _PERIODICVESTINGACCOUNT._serialized_options = b'\x88\xa0\x1f\x00\x98\xa0\x1f\x00\x8a\xe7\xb0*!cosmos-sdk/PeriodicVestingAccount'
    _PERMANENTLOCKEDACCOUNT.fields_by_name['base_vesting_account']._options = None
    _PERMANENTLOCKEDACCOUNT.fields_by_name['base_vesting_account']._serialized_options = b'\xd0\xde\x1f\x01'
    _PERMANENTLOCKEDACCOUNT._options = None
    _PERMANENTLOCKEDACCOUNT._serialized_options = b'\x88\xa0\x1f\x00\x98\xa0\x1f\x00\x8a\xe7\xb0*!cosmos-sdk/PermanentLockedAccount'
    _CLAWBACKVESTINGACCOUNT.fields_by_name['base_vesting_account']._options = None
    _CLAWBACKVESTINGACCOUNT.fields_by_name['base_vesting_account']._serialized_options = b'\xd0\xde\x1f\x01'
    _CLAWBACKVESTINGACCOUNT.fields_by_name['funder_address']._options = None
    _CLAWBACKVESTINGACCOUNT.fields_by_name['funder_address']._serialized_options = b'\xf2\xde\x1f\x15yaml:"funder_address"'
    _CLAWBACKVESTINGACCOUNT.fields_by_name['start_time']._options = None
    _CLAWBACKVESTINGACCOUNT.fields_by_name['start_time']._serialized_options = b'\xf2\xde\x1f\x11yaml:"start_time"'
    _CLAWBACKVESTINGACCOUNT.fields_by_name['lockup_periods']._options = None
    _CLAWBACKVESTINGACCOUNT.fields_by_name['lockup_periods']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x15yaml:"lockup_periods"'
    _CLAWBACKVESTINGACCOUNT.fields_by_name['vesting_periods']._options = None
    _CLAWBACKVESTINGACCOUNT.fields_by_name['vesting_periods']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x16yaml:"vesting_periods"'
    _CLAWBACKVESTINGACCOUNT._options = None
    _CLAWBACKVESTINGACCOUNT._serialized_options = b'\x88\xa0\x1f\x00\x98\xa0\x1f\x00'
    _globals['_BASEVESTINGACCOUNT']._serialized_start = 170
    _globals['_BASEVESTINGACCOUNT']._serialized_end = 637
    _globals['_CONTINUOUSVESTINGACCOUNT']._serialized_start = 640
    _globals['_CONTINUOUSVESTINGACCOUNT']._serialized_end = 816
    _globals['_DELAYEDVESTINGACCOUNT']._serialized_start = 819
    _globals['_DELAYEDVESTINGACCOUNT']._serialized_end = 969
    _globals['_PERIOD']._serialized_start = 972
    _globals['_PERIOD']._serialized_end = 1100
    _globals['_PERIODICVESTINGACCOUNT']._serialized_start = 1103
    _globals['_PERIODICVESTINGACCOUNT']._serialized_end = 1343
    _globals['_PERMANENTLOCKEDACCOUNT']._serialized_start = 1346
    _globals['_PERMANENTLOCKEDACCOUNT']._serialized_end = 1498
    _globals['_CLAWBACKVESTINGACCOUNT']._serialized_start = 1501
    _globals['_CLAWBACKVESTINGACCOUNT']._serialized_end = 1885