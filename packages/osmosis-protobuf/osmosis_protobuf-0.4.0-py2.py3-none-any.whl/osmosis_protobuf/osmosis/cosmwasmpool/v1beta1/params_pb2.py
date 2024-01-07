"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n)osmosis/cosmwasmpool/v1beta1/params.proto\x12\x1cosmosis.cosmwasmpool.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x1egoogle/protobuf/duration.proto"\x80\x01\n\x06Params\x127\n\x11code_id_whitelist\x18\x01 \x03(\x04B\x1c\xf2\xde\x1f\x18yaml:"code_id_whitelist"\x12=\n\x14pool_migration_limit\x18\x02 \x01(\x04B\x1f\xf2\xde\x1f\x1byaml:"pool_migration_limit"B:Z8github.com/osmosis-labs/osmosis/v21/x/cosmwasmpool/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.cosmwasmpool.v1beta1.params_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z8github.com/osmosis-labs/osmosis/v21/x/cosmwasmpool/types'
    _PARAMS.fields_by_name['code_id_whitelist']._options = None
    _PARAMS.fields_by_name['code_id_whitelist']._serialized_options = b'\xf2\xde\x1f\x18yaml:"code_id_whitelist"'
    _PARAMS.fields_by_name['pool_migration_limit']._options = None
    _PARAMS.fields_by_name['pool_migration_limit']._serialized_options = b'\xf2\xde\x1f\x1byaml:"pool_migration_limit"'
    _globals['_PARAMS']._serialized_start = 157
    _globals['_PARAMS']._serialized_end = 285