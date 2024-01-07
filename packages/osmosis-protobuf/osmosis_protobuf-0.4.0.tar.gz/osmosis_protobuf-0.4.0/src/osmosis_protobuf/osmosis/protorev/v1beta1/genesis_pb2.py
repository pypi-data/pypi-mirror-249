"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....osmosis.protorev.v1beta1 import protorev_pb2 as osmosis_dot_protorev_dot_v1beta1_dot_protorev__pb2
from ....osmosis.protorev.v1beta1 import params_pb2 as osmosis_dot_protorev_dot_v1beta1_dot_params__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&osmosis/protorev/v1beta1/genesis.proto\x12\x18osmosis.protorev.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\'osmosis/protorev/v1beta1/protorev.proto\x1a%osmosis/protorev/v1beta1/params.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x1ecosmos/base/v1beta1/coin.proto"\xeb\x08\n\x0cGenesisState\x126\n\x06params\x18\x01 \x01(\x0b2 .osmosis.protorev.v1beta1.ParamsB\x04\xc8\xde\x1f\x00\x12q\n\x15token_pair_arb_routes\x18\x02 \x03(\x0b2,.osmosis.protorev.v1beta1.TokenPairArbRoutesB$\xc8\xde\x1f\x00\xf2\xde\x1f\x1cyaml:"token_pair_arb_routes"\x12T\n\x0bbase_denoms\x18\x03 \x03(\x0b2#.osmosis.protorev.v1beta1.BaseDenomB\x1a\xc8\xde\x1f\x00\xf2\xde\x1f\x12yaml:"base_denoms"\x12X\n\x0cpool_weights\x18\x04 \x01(\x0b2%.osmosis.protorev.v1beta1.PoolWeightsB\x1b\xc8\xde\x1f\x00\xf2\xde\x1f\x13yaml:"pool_weights"\x12G\n\x19days_since_module_genesis\x18\x05 \x01(\x04B$\xf2\xde\x1f yaml:"days_since_module_genesis"\x12P\n\x0edeveloper_fees\x18\x06 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB\x1d\xc8\xde\x1f\x00\xf2\xde\x1f\x15yaml:"developer_fees"\x12;\n\x13latest_block_height\x18\x07 \x01(\x04B\x1e\xf2\xde\x1f\x1ayaml:"latest_block_height"\x12I\n\x11developer_address\x18\x08 \x01(\tB.\xf2\xde\x1f\x18yaml:"developer_address"\xd2\xb4-\x0ecosmos.Address\x12G\n\x19max_pool_points_per_block\x18\t \x01(\x04B$\xf2\xde\x1f yaml:"max_pool_points_per_block"\x12A\n\x16max_pool_points_per_tx\x18\n \x01(\x04B!\xf2\xde\x1f\x1dyaml:"max_pool_points_per_tx"\x12?\n\x15point_count_for_block\x18\x0b \x01(\x04B \xf2\xde\x1f\x1cyaml:"point_count_for_block"\x12B\n\x07profits\x18\x0c \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB\x16\xc8\xde\x1f\x00\xf2\xde\x1f\x0eyaml:"profits"\x12e\n\x11info_by_pool_type\x18\r \x01(\x0b2(.osmosis.protorev.v1beta1.InfoByPoolTypeB \xc8\xde\x1f\x00\xf2\xde\x1f\x18yaml:"info_by_pool_type"\x12e\n\x12cyclic_arb_tracker\x18\x0e \x01(\x0b2*.osmosis.protorev.v1beta1.CyclicArbTrackerB\x1d\xf2\xde\x1f\x19yaml:"cyclic_arb_tracker"B6Z4github.com/osmosis-labs/osmosis/v21/x/protorev/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.protorev.v1beta1.genesis_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z4github.com/osmosis-labs/osmosis/v21/x/protorev/types'
    _GENESISSTATE.fields_by_name['params']._options = None
    _GENESISSTATE.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['token_pair_arb_routes']._options = None
    _GENESISSTATE.fields_by_name['token_pair_arb_routes']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x1cyaml:"token_pair_arb_routes"'
    _GENESISSTATE.fields_by_name['base_denoms']._options = None
    _GENESISSTATE.fields_by_name['base_denoms']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x12yaml:"base_denoms"'
    _GENESISSTATE.fields_by_name['pool_weights']._options = None
    _GENESISSTATE.fields_by_name['pool_weights']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x13yaml:"pool_weights"'
    _GENESISSTATE.fields_by_name['days_since_module_genesis']._options = None
    _GENESISSTATE.fields_by_name['days_since_module_genesis']._serialized_options = b'\xf2\xde\x1f yaml:"days_since_module_genesis"'
    _GENESISSTATE.fields_by_name['developer_fees']._options = None
    _GENESISSTATE.fields_by_name['developer_fees']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x15yaml:"developer_fees"'
    _GENESISSTATE.fields_by_name['latest_block_height']._options = None
    _GENESISSTATE.fields_by_name['latest_block_height']._serialized_options = b'\xf2\xde\x1f\x1ayaml:"latest_block_height"'
    _GENESISSTATE.fields_by_name['developer_address']._options = None
    _GENESISSTATE.fields_by_name['developer_address']._serialized_options = b'\xf2\xde\x1f\x18yaml:"developer_address"\xd2\xb4-\x0ecosmos.Address'
    _GENESISSTATE.fields_by_name['max_pool_points_per_block']._options = None
    _GENESISSTATE.fields_by_name['max_pool_points_per_block']._serialized_options = b'\xf2\xde\x1f yaml:"max_pool_points_per_block"'
    _GENESISSTATE.fields_by_name['max_pool_points_per_tx']._options = None
    _GENESISSTATE.fields_by_name['max_pool_points_per_tx']._serialized_options = b'\xf2\xde\x1f\x1dyaml:"max_pool_points_per_tx"'
    _GENESISSTATE.fields_by_name['point_count_for_block']._options = None
    _GENESISSTATE.fields_by_name['point_count_for_block']._serialized_options = b'\xf2\xde\x1f\x1cyaml:"point_count_for_block"'
    _GENESISSTATE.fields_by_name['profits']._options = None
    _GENESISSTATE.fields_by_name['profits']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x0eyaml:"profits"'
    _GENESISSTATE.fields_by_name['info_by_pool_type']._options = None
    _GENESISSTATE.fields_by_name['info_by_pool_type']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x18yaml:"info_by_pool_type"'
    _GENESISSTATE.fields_by_name['cyclic_arb_tracker']._options = None
    _GENESISSTATE.fields_by_name['cyclic_arb_tracker']._serialized_options = b'\xf2\xde\x1f\x19yaml:"cyclic_arb_tracker"'
    _globals['_GENESISSTATE']._serialized_start = 230
    _globals['_GENESISSTATE']._serialized_end = 1361