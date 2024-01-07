"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from ....osmosis.poolmanager.v1beta1 import module_route_pb2 as osmosis_dot_poolmanager_dot_v1beta1_dot_module__route__pb2
from ....osmosis.poolmanager.v1beta1 import tx_pb2 as osmosis_dot_poolmanager_dot_v1beta1_dot_tx__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n)osmosis/poolmanager/v1beta1/genesis.proto\x12\x1bosmosis.poolmanager.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x19google/protobuf/any.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a.osmosis/poolmanager/v1beta1/module_route.proto\x1a$osmosis/poolmanager/v1beta1/tx.proto"\xba\x02\n\x06Params\x12\x82\x01\n\x11pool_creation_fee\x18\x01 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinBL\xc8\xde\x1f\x00\xf2\xde\x1f\x18yaml:"pool_creation_fee"\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x12f\n\x10taker_fee_params\x18\x02 \x01(\x0b2+.osmosis.poolmanager.v1beta1.TakerFeeParamsB\x1f\xc8\xde\x1f\x00\xf2\xde\x1f\x17yaml:"taker_fee_params"\x12C\n\x17authorized_quote_denoms\x18\x03 \x03(\tB"\xf2\xde\x1f\x1eyaml:"authorized_quote_denoms""\x88\x03\n\x0cGenesisState\x12\x14\n\x0cnext_pool_id\x18\x01 \x01(\x04\x129\n\x06params\x18\x02 \x01(\x0b2#.osmosis.poolmanager.v1beta1.ParamsB\x04\xc8\xde\x1f\x00\x12C\n\x0bpool_routes\x18\x03 \x03(\x0b2(.osmosis.poolmanager.v1beta1.ModuleRouteB\x04\xc8\xde\x1f\x00\x12I\n\x12taker_fees_tracker\x18\x04 \x01(\x0b2-.osmosis.poolmanager.v1beta1.TakerFeesTracker\x12=\n\x0cpool_volumes\x18\x05 \x03(\x0b2\'.osmosis.poolmanager.v1beta1.PoolVolume\x12X\n\x1adenom_pair_taker_fee_store\x18\x06 \x03(\x0b2..osmosis.poolmanager.v1beta1.DenomPairTakerFeeB\x04\xc8\xde\x1f\x00"\xee\x04\n\x0eTakerFeeParams\x12Q\n\x11default_taker_fee\x18\x01 \x01(\tB6\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xe2\xde\x1f\x0fDefaultTakerFee\x12\x82\x01\n\x1bosmo_taker_fee_distribution\x18\x02 \x01(\x0b2;.osmosis.poolmanager.v1beta1.TakerFeeDistributionPercentageB \xc8\xde\x1f\x00\xe2\xde\x1f\x18OsmoTakerFeeDistribution\x12\x89\x01\n\x1fnon_osmo_taker_fee_distribution\x18\x03 \x01(\x0b2;.osmosis.poolmanager.v1beta1.TakerFeeDistributionPercentageB#\xc8\xde\x1f\x00\xe2\xde\x1f\x1bNonOsmoTakerFeeDistribution\x123\n\x0fadmin_addresses\x18\x04 \x03(\tB\x1a\xf2\xde\x1f\x16yaml:"admin_addresses"\x12\x81\x01\n6community_pool_denom_to_swap_non_whitelisted_assets_to\x18\x05 \x01(\tBA\xf2\xde\x1f=yaml:"community_pool_denom_to_swap_non_whitelisted_assets_to"\x12?\n\x15reduced_fee_whitelist\x18\x06 \x03(\tB \xf2\xde\x1f\x1cyaml:"reduced_fee_whitelist""\xce\x01\n\x1eTakerFeeDistributionPercentage\x12V\n\x0fstaking_rewards\x18\x01 \x01(\tB=\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x16yaml:"staking_rewards"\x12T\n\x0ecommunity_pool\x18\x02 \x01(\tB<\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x15yaml:"community_pool""\xc2\x02\n\x10TakerFeesTracker\x12j\n\x15taker_fees_to_stakers\x18\x01 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x12q\n\x1ctaker_fees_to_community_pool\x18\x02 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x12O\n\x1dheight_accounting_starts_from\x18\x03 \x01(\x03B(\xf2\xde\x1f$yaml:"height_accounting_starts_from""\x7f\n\nPoolVolume\x12\x0f\n\x07pool_id\x18\x01 \x01(\x04\x12`\n\x0bpool_volume\x18\x02 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.CoinsB9Z7github.com/osmosis-labs/osmosis/v21/x/poolmanager/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.poolmanager.v1beta1.genesis_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z7github.com/osmosis-labs/osmosis/v21/x/poolmanager/types'
    _PARAMS.fields_by_name['pool_creation_fee']._options = None
    _PARAMS.fields_by_name['pool_creation_fee']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x18yaml:"pool_creation_fee"\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _PARAMS.fields_by_name['taker_fee_params']._options = None
    _PARAMS.fields_by_name['taker_fee_params']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x17yaml:"taker_fee_params"'
    _PARAMS.fields_by_name['authorized_quote_denoms']._options = None
    _PARAMS.fields_by_name['authorized_quote_denoms']._serialized_options = b'\xf2\xde\x1f\x1eyaml:"authorized_quote_denoms"'
    _GENESISSTATE.fields_by_name['params']._options = None
    _GENESISSTATE.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['pool_routes']._options = None
    _GENESISSTATE.fields_by_name['pool_routes']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['denom_pair_taker_fee_store']._options = None
    _GENESISSTATE.fields_by_name['denom_pair_taker_fee_store']._serialized_options = b'\xc8\xde\x1f\x00'
    _TAKERFEEPARAMS.fields_by_name['default_taker_fee']._options = None
    _TAKERFEEPARAMS.fields_by_name['default_taker_fee']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xe2\xde\x1f\x0fDefaultTakerFee'
    _TAKERFEEPARAMS.fields_by_name['osmo_taker_fee_distribution']._options = None
    _TAKERFEEPARAMS.fields_by_name['osmo_taker_fee_distribution']._serialized_options = b'\xc8\xde\x1f\x00\xe2\xde\x1f\x18OsmoTakerFeeDistribution'
    _TAKERFEEPARAMS.fields_by_name['non_osmo_taker_fee_distribution']._options = None
    _TAKERFEEPARAMS.fields_by_name['non_osmo_taker_fee_distribution']._serialized_options = b'\xc8\xde\x1f\x00\xe2\xde\x1f\x1bNonOsmoTakerFeeDistribution'
    _TAKERFEEPARAMS.fields_by_name['admin_addresses']._options = None
    _TAKERFEEPARAMS.fields_by_name['admin_addresses']._serialized_options = b'\xf2\xde\x1f\x16yaml:"admin_addresses"'
    _TAKERFEEPARAMS.fields_by_name['community_pool_denom_to_swap_non_whitelisted_assets_to']._options = None
    _TAKERFEEPARAMS.fields_by_name['community_pool_denom_to_swap_non_whitelisted_assets_to']._serialized_options = b'\xf2\xde\x1f=yaml:"community_pool_denom_to_swap_non_whitelisted_assets_to"'
    _TAKERFEEPARAMS.fields_by_name['reduced_fee_whitelist']._options = None
    _TAKERFEEPARAMS.fields_by_name['reduced_fee_whitelist']._serialized_options = b'\xf2\xde\x1f\x1cyaml:"reduced_fee_whitelist"'
    _TAKERFEEDISTRIBUTIONPERCENTAGE.fields_by_name['staking_rewards']._options = None
    _TAKERFEEDISTRIBUTIONPERCENTAGE.fields_by_name['staking_rewards']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x16yaml:"staking_rewards"'
    _TAKERFEEDISTRIBUTIONPERCENTAGE.fields_by_name['community_pool']._options = None
    _TAKERFEEDISTRIBUTIONPERCENTAGE.fields_by_name['community_pool']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x15yaml:"community_pool"'
    _TAKERFEESTRACKER.fields_by_name['taker_fees_to_stakers']._options = None
    _TAKERFEESTRACKER.fields_by_name['taker_fees_to_stakers']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _TAKERFEESTRACKER.fields_by_name['taker_fees_to_community_pool']._options = None
    _TAKERFEESTRACKER.fields_by_name['taker_fees_to_community_pool']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _TAKERFEESTRACKER.fields_by_name['height_accounting_starts_from']._options = None
    _TAKERFEESTRACKER.fields_by_name['height_accounting_starts_from']._serialized_options = b'\xf2\xde\x1f$yaml:"height_accounting_starts_from"'
    _POOLVOLUME.fields_by_name['pool_volume']._options = None
    _POOLVOLUME.fields_by_name['pool_volume']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _globals['_PARAMS']._serialized_start = 301
    _globals['_PARAMS']._serialized_end = 615
    _globals['_GENESISSTATE']._serialized_start = 618
    _globals['_GENESISSTATE']._serialized_end = 1010
    _globals['_TAKERFEEPARAMS']._serialized_start = 1013
    _globals['_TAKERFEEPARAMS']._serialized_end = 1635
    _globals['_TAKERFEEDISTRIBUTIONPERCENTAGE']._serialized_start = 1638
    _globals['_TAKERFEEDISTRIBUTIONPERCENTAGE']._serialized_end = 1844
    _globals['_TAKERFEESTRACKER']._serialized_start = 1847
    _globals['_TAKERFEESTRACKER']._serialized_end = 2169
    _globals['_POOLVOLUME']._serialized_start = 2171
    _globals['_POOLVOLUME']._serialized_end = 2298