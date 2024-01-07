"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%osmosis/protorev/v1beta1/params.proto\x12\x18osmosis.protorev.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x19cosmos_proto/cosmos.proto"N\n\x06Params\x12#\n\x07enabled\x18\x01 \x01(\x08B\x12\xf2\xde\x1f\x0eyaml:"enabled"\x12\x1f\n\x05admin\x18\x02 \x01(\tB\x10\xf2\xde\x1f\x0cyaml:"admin"B6Z4github.com/osmosis-labs/osmosis/v21/x/protorev/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.protorev.v1beta1.params_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z4github.com/osmosis-labs/osmosis/v21/x/protorev/types'
    _PARAMS.fields_by_name['enabled']._options = None
    _PARAMS.fields_by_name['enabled']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"enabled"'
    _PARAMS.fields_by_name['admin']._options = None
    _PARAMS.fields_by_name['admin']._serialized_options = b'\xf2\xde\x1f\x0cyaml:"admin"'
    _globals['_PARAMS']._serialized_start = 116
    _globals['_PARAMS']._serialized_end = 194