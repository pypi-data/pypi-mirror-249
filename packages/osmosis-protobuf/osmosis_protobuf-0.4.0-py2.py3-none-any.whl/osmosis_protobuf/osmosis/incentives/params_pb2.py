"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ...gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ...cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fosmosis/incentives/params.proto\x12\x12osmosis.incentives\x1a\x14gogoproto/gogo.proto\x1a\x1ecosmos/base/v1beta1/coin.proto"\x87\x02\n\x06Params\x12A\n\x16distr_epoch_identifier\x18\x01 \x01(\tB!\xf2\xde\x1f\x1dyaml:"distr_epoch_identifier"\x12g\n\x12group_creation_fee\x18\x02 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x12Q\n\x1eunrestricted_creator_whitelist\x18\x03 \x03(\tB)\xf2\xde\x1f%yaml:"unrestricted_creator_whitelist"B8Z6github.com/osmosis-labs/osmosis/v21/x/incentives/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.incentives.params_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z6github.com/osmosis-labs/osmosis/v21/x/incentives/types'
    _PARAMS.fields_by_name['distr_epoch_identifier']._options = None
    _PARAMS.fields_by_name['distr_epoch_identifier']._serialized_options = b'\xf2\xde\x1f\x1dyaml:"distr_epoch_identifier"'
    _PARAMS.fields_by_name['group_creation_fee']._options = None
    _PARAMS.fields_by_name['group_creation_fee']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _PARAMS.fields_by_name['unrestricted_creator_whitelist']._options = None
    _PARAMS.fields_by_name['unrestricted_creator_whitelist']._serialized_options = b'\xf2\xde\x1f%yaml:"unrestricted_creator_whitelist"'
    _globals['_PARAMS']._serialized_start = 110
    _globals['_PARAMS']._serialized_end = 373