"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from ....cosmwasm.wasm.v1 import types_pb2 as cosmwasm_dot_wasm_dot_v1_dot_types__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from ....amino import amino_pb2 as amino_dot_amino__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1ccosmwasm/wasm/v1/authz.proto\x12\x10cosmwasm.wasm.v1\x1a\x14gogoproto/gogo.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a\x1ccosmwasm/wasm/v1/types.proto\x1a\x19google/protobuf/any.proto\x1a\x11amino/amino.proto"\x98\x01\n\x16StoreCodeAuthorization\x126\n\x06grants\x18\x01 \x03(\x0b2\x1b.cosmwasm.wasm.v1.CodeGrantB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01:F\xca\xb4-"cosmos.authz.v1beta1.Authorization\x8a\xe7\xb0*\x1bwasm/StoreCodeAuthorization"\xac\x01\n\x1eContractExecutionAuthorization\x12:\n\x06grants\x18\x01 \x03(\x0b2\x1f.cosmwasm.wasm.v1.ContractGrantB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01:N\xca\xb4-"cosmos.authz.v1beta1.Authorization\x8a\xe7\xb0*#wasm/ContractExecutionAuthorization"\xac\x01\n\x1eContractMigrationAuthorization\x12:\n\x06grants\x18\x01 \x03(\x0b2\x1f.cosmwasm.wasm.v1.ContractGrantB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01:N\xca\xb4-"cosmos.authz.v1beta1.Authorization\x8a\xe7\xb0*#wasm/ContractMigrationAuthorization"^\n\tCodeGrant\x12\x11\n\tcode_hash\x18\x01 \x01(\x0c\x12>\n\x16instantiate_permission\x18\x02 \x01(\x0b2\x1e.cosmwasm.wasm.v1.AccessConfig"\xc1\x01\n\rContractGrant\x12\x10\n\x08contract\x18\x01 \x01(\t\x12M\n\x05limit\x18\x02 \x01(\x0b2\x14.google.protobuf.AnyB(\xca\xb4-$cosmwasm.wasm.v1.ContractAuthzLimitX\x12O\n\x06filter\x18\x03 \x01(\x0b2\x14.google.protobuf.AnyB)\xca\xb4-%cosmwasm.wasm.v1.ContractAuthzFilterX"c\n\rMaxCallsLimit\x12\x11\n\tremaining\x18\x01 \x01(\x04:?\xca\xb4-$cosmwasm.wasm.v1.ContractAuthzLimitX\x8a\xe7\xb0*\x12wasm/MaxCallsLimit"\xb3\x01\n\rMaxFundsLimit\x12a\n\x07amounts\x18\x01 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB5\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xa8\xe7\xb0*\x01:?\xca\xb4-$cosmwasm.wasm.v1.ContractAuthzLimitX\x8a\xe7\xb0*\x12wasm/MaxFundsLimit"\xcc\x01\n\rCombinedLimit\x12\x17\n\x0fcalls_remaining\x18\x01 \x01(\x04\x12a\n\x07amounts\x18\x02 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB5\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xa8\xe7\xb0*\x01:?\xca\xb4-$cosmwasm.wasm.v1.ContractAuthzLimitX\x8a\xe7\xb0*\x12wasm/CombinedLimit"c\n\x16AllowAllMessagesFilter:I\xca\xb4-%cosmwasm.wasm.v1.ContractAuthzFilterX\x8a\xe7\xb0*\x1bwasm/AllowAllMessagesFilter"w\n\x19AcceptedMessageKeysFilter\x12\x0c\n\x04keys\x18\x01 \x03(\t:L\xca\xb4-%cosmwasm.wasm.v1.ContractAuthzFilterX\x8a\xe7\xb0*\x1ewasm/AcceptedMessageKeysFilter"\x8d\x01\n\x16AcceptedMessagesFilter\x12(\n\x08messages\x18\x01 \x03(\x0cB\x16\xfa\xde\x1f\x12RawContractMessage:I\xca\xb4-%cosmwasm.wasm.v1.ContractAuthzFilterX\x8a\xe7\xb0*\x1bwasm/AcceptedMessagesFilterB,Z&github.com/CosmWasm/wasmd/x/wasm/types\xc8\xe1\x1e\x00b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmwasm.wasm.v1.authz_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z&github.com/CosmWasm/wasmd/x/wasm/types\xc8\xe1\x1e\x00'
    _STORECODEAUTHORIZATION.fields_by_name['grants']._options = None
    _STORECODEAUTHORIZATION.fields_by_name['grants']._serialized_options = b'\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01'
    _STORECODEAUTHORIZATION._options = None
    _STORECODEAUTHORIZATION._serialized_options = b'\xca\xb4-"cosmos.authz.v1beta1.Authorization\x8a\xe7\xb0*\x1bwasm/StoreCodeAuthorization'
    _CONTRACTEXECUTIONAUTHORIZATION.fields_by_name['grants']._options = None
    _CONTRACTEXECUTIONAUTHORIZATION.fields_by_name['grants']._serialized_options = b'\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01'
    _CONTRACTEXECUTIONAUTHORIZATION._options = None
    _CONTRACTEXECUTIONAUTHORIZATION._serialized_options = b'\xca\xb4-"cosmos.authz.v1beta1.Authorization\x8a\xe7\xb0*#wasm/ContractExecutionAuthorization'
    _CONTRACTMIGRATIONAUTHORIZATION.fields_by_name['grants']._options = None
    _CONTRACTMIGRATIONAUTHORIZATION.fields_by_name['grants']._serialized_options = b'\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01'
    _CONTRACTMIGRATIONAUTHORIZATION._options = None
    _CONTRACTMIGRATIONAUTHORIZATION._serialized_options = b'\xca\xb4-"cosmos.authz.v1beta1.Authorization\x8a\xe7\xb0*#wasm/ContractMigrationAuthorization'
    _CONTRACTGRANT.fields_by_name['limit']._options = None
    _CONTRACTGRANT.fields_by_name['limit']._serialized_options = b'\xca\xb4-$cosmwasm.wasm.v1.ContractAuthzLimitX'
    _CONTRACTGRANT.fields_by_name['filter']._options = None
    _CONTRACTGRANT.fields_by_name['filter']._serialized_options = b'\xca\xb4-%cosmwasm.wasm.v1.ContractAuthzFilterX'
    _MAXCALLSLIMIT._options = None
    _MAXCALLSLIMIT._serialized_options = b'\xca\xb4-$cosmwasm.wasm.v1.ContractAuthzLimitX\x8a\xe7\xb0*\x12wasm/MaxCallsLimit'
    _MAXFUNDSLIMIT.fields_by_name['amounts']._options = None
    _MAXFUNDSLIMIT.fields_by_name['amounts']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xa8\xe7\xb0*\x01'
    _MAXFUNDSLIMIT._options = None
    _MAXFUNDSLIMIT._serialized_options = b'\xca\xb4-$cosmwasm.wasm.v1.ContractAuthzLimitX\x8a\xe7\xb0*\x12wasm/MaxFundsLimit'
    _COMBINEDLIMIT.fields_by_name['amounts']._options = None
    _COMBINEDLIMIT.fields_by_name['amounts']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xa8\xe7\xb0*\x01'
    _COMBINEDLIMIT._options = None
    _COMBINEDLIMIT._serialized_options = b'\xca\xb4-$cosmwasm.wasm.v1.ContractAuthzLimitX\x8a\xe7\xb0*\x12wasm/CombinedLimit'
    _ALLOWALLMESSAGESFILTER._options = None
    _ALLOWALLMESSAGESFILTER._serialized_options = b'\xca\xb4-%cosmwasm.wasm.v1.ContractAuthzFilterX\x8a\xe7\xb0*\x1bwasm/AllowAllMessagesFilter'
    _ACCEPTEDMESSAGEKEYSFILTER._options = None
    _ACCEPTEDMESSAGEKEYSFILTER._serialized_options = b'\xca\xb4-%cosmwasm.wasm.v1.ContractAuthzFilterX\x8a\xe7\xb0*\x1ewasm/AcceptedMessageKeysFilter'
    _ACCEPTEDMESSAGESFILTER.fields_by_name['messages']._options = None
    _ACCEPTEDMESSAGESFILTER.fields_by_name['messages']._serialized_options = b'\xfa\xde\x1f\x12RawContractMessage'
    _ACCEPTEDMESSAGESFILTER._options = None
    _ACCEPTEDMESSAGESFILTER._serialized_options = b'\xca\xb4-%cosmwasm.wasm.v1.ContractAuthzFilterX\x8a\xe7\xb0*\x1bwasm/AcceptedMessagesFilter'
    _globals['_STORECODEAUTHORIZATION']._serialized_start = 208
    _globals['_STORECODEAUTHORIZATION']._serialized_end = 360
    _globals['_CONTRACTEXECUTIONAUTHORIZATION']._serialized_start = 363
    _globals['_CONTRACTEXECUTIONAUTHORIZATION']._serialized_end = 535
    _globals['_CONTRACTMIGRATIONAUTHORIZATION']._serialized_start = 538
    _globals['_CONTRACTMIGRATIONAUTHORIZATION']._serialized_end = 710
    _globals['_CODEGRANT']._serialized_start = 712
    _globals['_CODEGRANT']._serialized_end = 806
    _globals['_CONTRACTGRANT']._serialized_start = 809
    _globals['_CONTRACTGRANT']._serialized_end = 1002
    _globals['_MAXCALLSLIMIT']._serialized_start = 1004
    _globals['_MAXCALLSLIMIT']._serialized_end = 1103
    _globals['_MAXFUNDSLIMIT']._serialized_start = 1106
    _globals['_MAXFUNDSLIMIT']._serialized_end = 1285
    _globals['_COMBINEDLIMIT']._serialized_start = 1288
    _globals['_COMBINEDLIMIT']._serialized_end = 1492
    _globals['_ALLOWALLMESSAGESFILTER']._serialized_start = 1494
    _globals['_ALLOWALLMESSAGESFILTER']._serialized_end = 1593
    _globals['_ACCEPTEDMESSAGEKEYSFILTER']._serialized_start = 1595
    _globals['_ACCEPTEDMESSAGEKEYSFILTER']._serialized_end = 1714
    _globals['_ACCEPTEDMESSAGESFILTER']._serialized_start = 1717
    _globals['_ACCEPTEDMESSAGESFILTER']._serialized_end = 1858