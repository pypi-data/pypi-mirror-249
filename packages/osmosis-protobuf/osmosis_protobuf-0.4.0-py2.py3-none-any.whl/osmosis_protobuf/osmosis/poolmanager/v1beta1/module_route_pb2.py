"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n.osmosis/poolmanager/v1beta1/module_route.proto\x12\x1bosmosis.poolmanager.v1beta1\x1a\x14gogoproto/gogo.proto"p\n\x0bModuleRoute\x128\n\tpool_type\x18\x01 \x01(\x0e2%.osmosis.poolmanager.v1beta1.PoolType\x12\'\n\x07pool_id\x18\x02 \x01(\x04B\x16\xc8\xde\x1f\x01\xf2\xde\x1f\x0eyaml:"pool_id"*N\n\x08PoolType\x12\x0c\n\x08Balancer\x10\x00\x12\x0e\n\nStableswap\x10\x01\x12\x10\n\x0cConcentrated\x10\x02\x12\x0c\n\x08CosmWasm\x10\x03\x1a\x04\x88\xa3\x1e\x00B9Z7github.com/osmosis-labs/osmosis/v21/x/poolmanager/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.poolmanager.v1beta1.module_route_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z7github.com/osmosis-labs/osmosis/v21/x/poolmanager/types'
    _POOLTYPE._options = None
    _POOLTYPE._serialized_options = b'\x88\xa3\x1e\x00'
    _MODULEROUTE.fields_by_name['pool_id']._options = None
    _MODULEROUTE.fields_by_name['pool_id']._serialized_options = b'\xc8\xde\x1f\x01\xf2\xde\x1f\x0eyaml:"pool_id"'
    _globals['_POOLTYPE']._serialized_start = 215
    _globals['_POOLTYPE']._serialized_end = 293
    _globals['_MODULEROUTE']._serialized_start = 101
    _globals['_MODULEROUTE']._serialized_end = 213