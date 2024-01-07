"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!osmosis/accum/v1beta1/accum.proto\x12\x15osmosis.accum.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x1ecosmos/base/v1beta1/coin.proto"\xb7\x01\n\x12AccumulatorContent\x12f\n\x0baccum_value\x18\x01 \x03(\x0b2\x1c.cosmos.base.v1beta1.DecCoinB3\xc8\xde\x1f\x00\xaa\xdf\x1f+github.com/cosmos/cosmos-sdk/types.DecCoins\x129\n\x0ctotal_shares\x18\x02 \x01(\tB#\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec"\t\n\x07Options"\xd8\x02\n\x06Record\x127\n\nnum_shares\x18\x01 \x01(\tB#\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\x12p\n\x15accum_value_per_share\x18\x02 \x03(\x0b2\x1c.cosmos.base.v1beta1.DecCoinB3\xc8\xde\x1f\x00\xaa\xdf\x1f+github.com/cosmos/cosmos-sdk/types.DecCoins\x12r\n\x17unclaimed_rewards_total\x18\x03 \x03(\x0b2\x1c.cosmos.base.v1beta1.DecCoinB3\xc8\xde\x1f\x00\xaa\xdf\x1f+github.com/cosmos/cosmos-sdk/types.DecCoins\x12/\n\x07options\x18\x04 \x01(\x0b2\x1e.osmosis.accum.v1beta1.OptionsB1Z/github.com/osmosis-labs/osmosis/osmoutils/accumb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.accum.v1beta1.accum_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z/github.com/osmosis-labs/osmosis/osmoutils/accum'
    _ACCUMULATORCONTENT.fields_by_name['accum_value']._options = None
    _ACCUMULATORCONTENT.fields_by_name['accum_value']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f+github.com/cosmos/cosmos-sdk/types.DecCoins'
    _ACCUMULATORCONTENT.fields_by_name['total_shares']._options = None
    _ACCUMULATORCONTENT.fields_by_name['total_shares']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec'
    _RECORD.fields_by_name['num_shares']._options = None
    _RECORD.fields_by_name['num_shares']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec'
    _RECORD.fields_by_name['accum_value_per_share']._options = None
    _RECORD.fields_by_name['accum_value_per_share']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f+github.com/cosmos/cosmos-sdk/types.DecCoins'
    _RECORD.fields_by_name['unclaimed_rewards_total']._options = None
    _RECORD.fields_by_name['unclaimed_rewards_total']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f+github.com/cosmos/cosmos-sdk/types.DecCoins'
    _globals['_ACCUMULATORCONTENT']._serialized_start = 115
    _globals['_ACCUMULATORCONTENT']._serialized_end = 298
    _globals['_OPTIONS']._serialized_start = 300
    _globals['_OPTIONS']._serialized_end = 309
    _globals['_RECORD']._serialized_start = 312
    _globals['_RECORD']._serialized_end = 656