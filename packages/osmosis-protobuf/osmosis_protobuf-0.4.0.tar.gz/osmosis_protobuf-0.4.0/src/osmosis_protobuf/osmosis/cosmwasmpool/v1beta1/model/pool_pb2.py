"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from .....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from .....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n-osmosis/cosmwasmpool/v1beta1/model/pool.proto\x12\x1cosmosis.cosmwasmpool.v1beta1\x1a\x19cosmos_proto/cosmos.proto\x1a\x14gogoproto/gogo.proto\x1a\x1fgoogle/protobuf/timestamp.proto"\xaf\x01\n\x0cCosmWasmPool\x125\n\x10contract_address\x18\x01 \x01(\tB\x1b\xf2\xde\x1f\x17yaml:"contract_address"\x12\x0f\n\x07pool_id\x18\x02 \x01(\x04\x12\x0f\n\x07code_id\x18\x03 \x01(\x04\x123\n\x0finstantiate_msg\x18\x04 \x01(\x0cB\x1a\xf2\xde\x1f\x16yaml:"instantiate_msg":\x11\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xca\xb4-\x05PoolIB:Z8github.com/osmosis-labs/osmosis/v21/x/cosmwasmpool/modelb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.cosmwasmpool.v1beta1.model.pool_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z8github.com/osmosis-labs/osmosis/v21/x/cosmwasmpool/model'
    _COSMWASMPOOL.fields_by_name['contract_address']._options = None
    _COSMWASMPOOL.fields_by_name['contract_address']._serialized_options = b'\xf2\xde\x1f\x17yaml:"contract_address"'
    _COSMWASMPOOL.fields_by_name['instantiate_msg']._options = None
    _COSMWASMPOOL.fields_by_name['instantiate_msg']._serialized_options = b'\xf2\xde\x1f\x16yaml:"instantiate_msg"'
    _COSMWASMPOOL._options = None
    _COSMWASMPOOL._serialized_options = b'\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xca\xb4-\x05PoolI'
    _globals['_COSMWASMPOOL']._serialized_start = 162
    _globals['_COSMWASMPOOL']._serialized_end = 337