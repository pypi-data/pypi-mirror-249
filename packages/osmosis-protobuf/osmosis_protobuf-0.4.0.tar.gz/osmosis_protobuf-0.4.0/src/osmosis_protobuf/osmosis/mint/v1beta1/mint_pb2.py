"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fosmosis/mint/v1beta1/mint.proto\x12\x14osmosis.mint.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x19google/protobuf/any.proto\x1a\x1egoogle/protobuf/duration.proto"b\n\x06Minter\x12X\n\x10epoch_provisions\x18\x01 \x01(\tB>\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x17yaml:"epoch_provisions""|\n\x0fWeightedAddress\x12#\n\x07address\x18\x01 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:"address"\x12D\n\x06weight\x18\x02 \x01(\tB4\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\ryaml:"weight""\xeb\x02\n\x17DistributionProportions\x12F\n\x07staking\x18\x01 \x01(\tB5\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x0eyaml:"staking"\x12V\n\x0fpool_incentives\x18\x02 \x01(\tB=\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x16yaml:"pool_incentives"\x12Z\n\x11developer_rewards\x18\x03 \x01(\tB?\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x18yaml:"developer_rewards"\x12T\n\x0ecommunity_pool\x18\x04 \x01(\tB<\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x15yaml:"community_pool""\xa6\x05\n\x06Params\x12\x12\n\nmint_denom\x18\x01 \x01(\t\x12h\n\x18genesis_epoch_provisions\x18\x02 \x01(\tBF\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x1fyaml:"genesis_epoch_provisions"\x125\n\x10epoch_identifier\x18\x03 \x01(\tB\x1b\xf2\xde\x1f\x17yaml:"epoch_identifier"\x12I\n\x1areduction_period_in_epochs\x18\x04 \x01(\x03B%\xf2\xde\x1f!yaml:"reduction_period_in_epochs"\x12X\n\x10reduction_factor\x18\x05 \x01(\tB>\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x17yaml:"reduction_factor"\x12U\n\x18distribution_proportions\x18\x06 \x01(\x0b2-.osmosis.mint.v1beta1.DistributionProportionsB\x04\xc8\xde\x1f\x00\x12~\n$weighted_developer_rewards_receivers\x18\x07 \x03(\x0b2%.osmosis.mint.v1beta1.WeightedAddressB)\xc8\xde\x1f\x00\xf2\xde\x1f!yaml:"developer_rewards_receiver"\x12e\n(minting_rewards_distribution_start_epoch\x18\x08 \x01(\x03B3\xf2\xde\x1f/yaml:"minting_rewards_distribution_start_epoch":\x04\x98\xa0\x1f\x00B2Z0github.com/osmosis-labs/osmosis/v21/x/mint/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.mint.v1beta1.mint_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z0github.com/osmosis-labs/osmosis/v21/x/mint/types'
    _MINTER.fields_by_name['epoch_provisions']._options = None
    _MINTER.fields_by_name['epoch_provisions']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x17yaml:"epoch_provisions"'
    _WEIGHTEDADDRESS.fields_by_name['address']._options = None
    _WEIGHTEDADDRESS.fields_by_name['address']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"address"'
    _WEIGHTEDADDRESS.fields_by_name['weight']._options = None
    _WEIGHTEDADDRESS.fields_by_name['weight']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\ryaml:"weight"'
    _DISTRIBUTIONPROPORTIONS.fields_by_name['staking']._options = None
    _DISTRIBUTIONPROPORTIONS.fields_by_name['staking']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x0eyaml:"staking"'
    _DISTRIBUTIONPROPORTIONS.fields_by_name['pool_incentives']._options = None
    _DISTRIBUTIONPROPORTIONS.fields_by_name['pool_incentives']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x16yaml:"pool_incentives"'
    _DISTRIBUTIONPROPORTIONS.fields_by_name['developer_rewards']._options = None
    _DISTRIBUTIONPROPORTIONS.fields_by_name['developer_rewards']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x18yaml:"developer_rewards"'
    _DISTRIBUTIONPROPORTIONS.fields_by_name['community_pool']._options = None
    _DISTRIBUTIONPROPORTIONS.fields_by_name['community_pool']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x15yaml:"community_pool"'
    _PARAMS.fields_by_name['genesis_epoch_provisions']._options = None
    _PARAMS.fields_by_name['genesis_epoch_provisions']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x1fyaml:"genesis_epoch_provisions"'
    _PARAMS.fields_by_name['epoch_identifier']._options = None
    _PARAMS.fields_by_name['epoch_identifier']._serialized_options = b'\xf2\xde\x1f\x17yaml:"epoch_identifier"'
    _PARAMS.fields_by_name['reduction_period_in_epochs']._options = None
    _PARAMS.fields_by_name['reduction_period_in_epochs']._serialized_options = b'\xf2\xde\x1f!yaml:"reduction_period_in_epochs"'
    _PARAMS.fields_by_name['reduction_factor']._options = None
    _PARAMS.fields_by_name['reduction_factor']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x17yaml:"reduction_factor"'
    _PARAMS.fields_by_name['distribution_proportions']._options = None
    _PARAMS.fields_by_name['distribution_proportions']._serialized_options = b'\xc8\xde\x1f\x00'
    _PARAMS.fields_by_name['weighted_developer_rewards_receivers']._options = None
    _PARAMS.fields_by_name['weighted_developer_rewards_receivers']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f!yaml:"developer_rewards_receiver"'
    _PARAMS.fields_by_name['minting_rewards_distribution_start_epoch']._options = None
    _PARAMS.fields_by_name['minting_rewards_distribution_start_epoch']._serialized_options = b'\xf2\xde\x1f/yaml:"minting_rewards_distribution_start_epoch"'
    _PARAMS._options = None
    _PARAMS._serialized_options = b'\x98\xa0\x1f\x00'
    _globals['_MINTER']._serialized_start = 171
    _globals['_MINTER']._serialized_end = 269
    _globals['_WEIGHTEDADDRESS']._serialized_start = 271
    _globals['_WEIGHTEDADDRESS']._serialized_end = 395
    _globals['_DISTRIBUTIONPROPORTIONS']._serialized_start = 398
    _globals['_DISTRIBUTIONPROPORTIONS']._serialized_end = 761
    _globals['_PARAMS']._serialized_start = 764
    _globals['_PARAMS']._serialized_end = 1442