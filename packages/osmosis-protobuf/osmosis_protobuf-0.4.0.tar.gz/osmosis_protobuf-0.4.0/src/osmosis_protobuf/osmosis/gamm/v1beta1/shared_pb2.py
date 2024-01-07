"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!osmosis/gamm/v1beta1/shared.proto\x12\x14osmosis.gamm.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x19google/protobuf/any.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x1ecosmos/base/v1beta1/coin.proto"{\n\x10MigrationRecords\x12g\n#balancer_to_concentrated_pool_links\x18\x01 \x03(\x0b24.osmosis.gamm.v1beta1.BalancerToConcentratedPoolLinkB\x04\xc8\xde\x1f\x00"T\n\x1eBalancerToConcentratedPoolLink\x12\x18\n\x10balancer_pool_id\x18\x01 \x01(\x04\x12\x12\n\ncl_pool_id\x18\x02 \x01(\x04:\x04\xe8\xa0\x1f\x01B<Z:github.com/osmosis-labs/osmosis/v21/x/gamm/types/migrationb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.gamm.v1beta1.shared_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z:github.com/osmosis-labs/osmosis/v21/x/gamm/types/migration'
    _MIGRATIONRECORDS.fields_by_name['balancer_to_concentrated_pool_links']._options = None
    _MIGRATIONRECORDS.fields_by_name['balancer_to_concentrated_pool_links']._serialized_options = b'\xc8\xde\x1f\x00'
    _BALANCERTOCONCENTRATEDPOOLLINK._options = None
    _BALANCERTOCONCENTRATEDPOOLLINK._serialized_options = b'\xe8\xa0\x1f\x01'
    _globals['_MIGRATIONRECORDS']._serialized_start = 167
    _globals['_MIGRATIONRECORDS']._serialized_end = 290
    _globals['_BALANCERTOCONCENTRATEDPOOLLINK']._serialized_start = 292
    _globals['_BALANCERTOCONCENTRATEDPOOLLINK']._serialized_end = 376