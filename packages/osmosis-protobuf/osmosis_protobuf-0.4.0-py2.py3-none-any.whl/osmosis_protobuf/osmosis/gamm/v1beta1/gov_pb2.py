"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....osmosis.gamm.v1beta1 import genesis_pb2 as osmosis_dot_gamm_dot_v1beta1_dot_genesis__pb2
from ....osmosis.gamm.v1beta1 import shared_pb2 as osmosis_dot_gamm_dot_v1beta1_dot_shared__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from ....amino import amino_pb2 as amino_dot_amino__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1eosmosis/gamm/v1beta1/gov.proto\x12\x14osmosis.gamm.v1beta1\x1a\x14gogoproto/gogo.proto\x1a"osmosis/gamm/v1beta1/genesis.proto\x1a!osmosis/gamm/v1beta1/shared.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x11amino/amino.proto"\xea\x01\n\x1fReplaceMigrationRecordsProposal\x12\r\n\x05title\x18\x01 \x01(\t\x12\x13\n\x0bdescription\x18\x02 \x01(\t\x12K\n\x07records\x18\x03 \x03(\x0b24.osmosis.gamm.v1beta1.BalancerToConcentratedPoolLinkB\x04\xc8\xde\x1f\x00:V\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xe8\xa0\x1f\x01\xca\xb4-\x1acosmos.gov.v1beta1.Content\x8a\xe7\xb0*\'osmosis/ReplaceMigrationRecordsProposal"\xe8\x01\n\x1eUpdateMigrationRecordsProposal\x12\r\n\x05title\x18\x01 \x01(\t\x12\x13\n\x0bdescription\x18\x02 \x01(\t\x12K\n\x07records\x18\x03 \x03(\x0b24.osmosis.gamm.v1beta1.BalancerToConcentratedPoolLinkB\x04\xc8\xde\x1f\x00:U\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xe8\xa0\x1f\x01\xca\xb4-\x1acosmos.gov.v1beta1.Content\x8a\xe7\xb0*&osmosis/UpdateMigrationRecordsProposal"\xfc\x02\n\x16PoolRecordWithCFMMLink\x12!\n\x06denom0\x18\x01 \x01(\tB\x11\xf2\xde\x1f\ryaml:"denom0"\x12!\n\x06denom1\x18\x02 \x01(\tB\x11\xf2\xde\x1f\ryaml:"denom1"\x12-\n\x0ctick_spacing\x18\x03 \x01(\x04B\x17\xf2\xde\x1f\x13yaml:"tick_spacing"\x12\\\n\x15exponent_at_price_one\x18\x04 \x01(\tB=\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x1cyaml:"exponent_at_price_one"\x12R\n\rspread_factor\x18\x05 \x01(\tB;\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x14yaml:"spread_factor"\x125\n\x10balancer_pool_id\x18\x06 \x01(\x04B\x1b\xf2\xde\x1f\x17yaml:"balancer_pool_id":\x04\xe8\xa0\x1f\x01"\xcd\x02\n5CreateConcentratedLiquidityPoolsAndLinktoCFMMProposal\x12\r\n\x05title\x18\x01 \x01(\t\x12\x13\n\x0bdescription\x18\x02 \x01(\t\x12\x81\x01\n\x1bpool_records_with_cfmm_link\x18\x03 \x03(\x0b2,.osmosis.gamm.v1beta1.PoolRecordWithCFMMLinkB.\xc8\xde\x1f\x00\xf2\xde\x1f&yaml:"create_cl_pool_and_link_to_cfmm":l\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xe8\xa0\x1f\x01\xca\xb4-\x1acosmos.gov.v1beta1.Content\x8a\xe7\xb0*=osmosis/CreateConcentratedLiquidityPoolsAndLinktoCFMMProposal"\xd0\x01\n"SetScalingFactorControllerProposal\x12\r\n\x05title\x18\x01 \x01(\t\x12\x13\n\x0bdescription\x18\x02 \x01(\t\x12\x0f\n\x07pool_id\x18\x03 \x01(\x04\x12\x1a\n\x12controller_address\x18\x04 \x01(\t:Y\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xe8\xa0\x1f\x01\xca\xb4-\x1acosmos.gov.v1beta1.Content\x8a\xe7\xb0**osmosis/SetScalingFactorControllerProposalB2Z0github.com/osmosis-labs/osmosis/v21/x/gamm/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.gamm.v1beta1.gov_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z0github.com/osmosis-labs/osmosis/v21/x/gamm/types'
    _REPLACEMIGRATIONRECORDSPROPOSAL.fields_by_name['records']._options = None
    _REPLACEMIGRATIONRECORDSPROPOSAL.fields_by_name['records']._serialized_options = b'\xc8\xde\x1f\x00'
    _REPLACEMIGRATIONRECORDSPROPOSAL._options = None
    _REPLACEMIGRATIONRECORDSPROPOSAL._serialized_options = b"\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xe8\xa0\x1f\x01\xca\xb4-\x1acosmos.gov.v1beta1.Content\x8a\xe7\xb0*'osmosis/ReplaceMigrationRecordsProposal"
    _UPDATEMIGRATIONRECORDSPROPOSAL.fields_by_name['records']._options = None
    _UPDATEMIGRATIONRECORDSPROPOSAL.fields_by_name['records']._serialized_options = b'\xc8\xde\x1f\x00'
    _UPDATEMIGRATIONRECORDSPROPOSAL._options = None
    _UPDATEMIGRATIONRECORDSPROPOSAL._serialized_options = b'\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xe8\xa0\x1f\x01\xca\xb4-\x1acosmos.gov.v1beta1.Content\x8a\xe7\xb0*&osmosis/UpdateMigrationRecordsProposal'
    _POOLRECORDWITHCFMMLINK.fields_by_name['denom0']._options = None
    _POOLRECORDWITHCFMMLINK.fields_by_name['denom0']._serialized_options = b'\xf2\xde\x1f\ryaml:"denom0"'
    _POOLRECORDWITHCFMMLINK.fields_by_name['denom1']._options = None
    _POOLRECORDWITHCFMMLINK.fields_by_name['denom1']._serialized_options = b'\xf2\xde\x1f\ryaml:"denom1"'
    _POOLRECORDWITHCFMMLINK.fields_by_name['tick_spacing']._options = None
    _POOLRECORDWITHCFMMLINK.fields_by_name['tick_spacing']._serialized_options = b'\xf2\xde\x1f\x13yaml:"tick_spacing"'
    _POOLRECORDWITHCFMMLINK.fields_by_name['exponent_at_price_one']._options = None
    _POOLRECORDWITHCFMMLINK.fields_by_name['exponent_at_price_one']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x1cyaml:"exponent_at_price_one"'
    _POOLRECORDWITHCFMMLINK.fields_by_name['spread_factor']._options = None
    _POOLRECORDWITHCFMMLINK.fields_by_name['spread_factor']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x14yaml:"spread_factor"'
    _POOLRECORDWITHCFMMLINK.fields_by_name['balancer_pool_id']._options = None
    _POOLRECORDWITHCFMMLINK.fields_by_name['balancer_pool_id']._serialized_options = b'\xf2\xde\x1f\x17yaml:"balancer_pool_id"'
    _POOLRECORDWITHCFMMLINK._options = None
    _POOLRECORDWITHCFMMLINK._serialized_options = b'\xe8\xa0\x1f\x01'
    _CREATECONCENTRATEDLIQUIDITYPOOLSANDLINKTOCFMMPROPOSAL.fields_by_name['pool_records_with_cfmm_link']._options = None
    _CREATECONCENTRATEDLIQUIDITYPOOLSANDLINKTOCFMMPROPOSAL.fields_by_name['pool_records_with_cfmm_link']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f&yaml:"create_cl_pool_and_link_to_cfmm"'
    _CREATECONCENTRATEDLIQUIDITYPOOLSANDLINKTOCFMMPROPOSAL._options = None
    _CREATECONCENTRATEDLIQUIDITYPOOLSANDLINKTOCFMMPROPOSAL._serialized_options = b'\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xe8\xa0\x1f\x01\xca\xb4-\x1acosmos.gov.v1beta1.Content\x8a\xe7\xb0*=osmosis/CreateConcentratedLiquidityPoolsAndLinktoCFMMProposal'
    _SETSCALINGFACTORCONTROLLERPROPOSAL._options = None
    _SETSCALINGFACTORCONTROLLERPROPOSAL._serialized_options = b'\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xe8\xa0\x1f\x01\xca\xb4-\x1acosmos.gov.v1beta1.Content\x8a\xe7\xb0**osmosis/SetScalingFactorControllerProposal'
    _globals['_REPLACEMIGRATIONRECORDSPROPOSAL']._serialized_start = 196
    _globals['_REPLACEMIGRATIONRECORDSPROPOSAL']._serialized_end = 430
    _globals['_UPDATEMIGRATIONRECORDSPROPOSAL']._serialized_start = 433
    _globals['_UPDATEMIGRATIONRECORDSPROPOSAL']._serialized_end = 665
    _globals['_POOLRECORDWITHCFMMLINK']._serialized_start = 668
    _globals['_POOLRECORDWITHCFMMLINK']._serialized_end = 1048
    _globals['_CREATECONCENTRATEDLIQUIDITYPOOLSANDLINKTOCFMMPROPOSAL']._serialized_start = 1051
    _globals['_CREATECONCENTRATEDLIQUIDITYPOOLSANDLINKTOCFMMPROPOSAL']._serialized_end = 1384
    _globals['_SETSCALINGFACTORCONTROLLERPROPOSAL']._serialized_start = 1387
    _globals['_SETSCALINGFACTORCONTROLLERPROPOSAL']._serialized_end = 1595