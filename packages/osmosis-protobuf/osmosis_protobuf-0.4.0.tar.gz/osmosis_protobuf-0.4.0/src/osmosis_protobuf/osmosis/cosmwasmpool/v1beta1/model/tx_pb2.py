"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from .....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from .....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n+osmosis/cosmwasmpool/v1beta1/model/tx.proto\x12\x1cosmosis.cosmwasmpool.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x1ecosmos/base/v1beta1/coin.proto"\x94\x01\n\x15MsgCreateCosmWasmPool\x12#\n\x07code_id\x18\x01 \x01(\x04B\x12\xf2\xde\x1f\x0eyaml:"code_id"\x123\n\x0finstantiate_msg\x18\x02 \x01(\x0cB\x1a\xf2\xde\x1f\x16yaml:"instantiate_msg"\x12!\n\x06sender\x18\x03 \x01(\tB\x11\xf2\xde\x1f\ryaml:"sender""<\n\x1dMsgCreateCosmWasmPoolResponse\x12\x1b\n\x07pool_id\x18\x01 \x01(\x04B\n\xe2\xde\x1f\x06PoolID2\x95\x01\n\nMsgCreator\x12\x86\x01\n\x12CreateCosmWasmPool\x123.osmosis.cosmwasmpool.v1beta1.MsgCreateCosmWasmPool\x1a;.osmosis.cosmwasmpool.v1beta1.MsgCreateCosmWasmPoolResponseB:Z8github.com/osmosis-labs/osmosis/v21/x/cosmwasmpool/modelb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.cosmwasmpool.v1beta1.model.tx_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z8github.com/osmosis-labs/osmosis/v21/x/cosmwasmpool/model'
    _MSGCREATECOSMWASMPOOL.fields_by_name['code_id']._options = None
    _MSGCREATECOSMWASMPOOL.fields_by_name['code_id']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"code_id"'
    _MSGCREATECOSMWASMPOOL.fields_by_name['instantiate_msg']._options = None
    _MSGCREATECOSMWASMPOOL.fields_by_name['instantiate_msg']._serialized_options = b'\xf2\xde\x1f\x16yaml:"instantiate_msg"'
    _MSGCREATECOSMWASMPOOL.fields_by_name['sender']._options = None
    _MSGCREATECOSMWASMPOOL.fields_by_name['sender']._serialized_options = b'\xf2\xde\x1f\ryaml:"sender"'
    _MSGCREATECOSMWASMPOOLRESPONSE.fields_by_name['pool_id']._options = None
    _MSGCREATECOSMWASMPOOLRESPONSE.fields_by_name['pool_id']._serialized_options = b'\xe2\xde\x1f\x06PoolID'
    _globals['_MSGCREATECOSMWASMPOOL']._serialized_start = 132
    _globals['_MSGCREATECOSMWASMPOOL']._serialized_end = 280
    _globals['_MSGCREATECOSMWASMPOOLRESPONSE']._serialized_start = 282
    _globals['_MSGCREATECOSMWASMPOOLRESPONSE']._serialized_end = 342
    _globals['_MSGCREATOR']._serialized_start = 345
    _globals['_MSGCREATOR']._serialized_end = 494