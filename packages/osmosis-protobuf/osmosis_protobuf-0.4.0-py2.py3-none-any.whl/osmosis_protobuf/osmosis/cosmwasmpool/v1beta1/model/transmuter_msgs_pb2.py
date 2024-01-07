"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from .....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from .....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n8osmosis/cosmwasmpool/v1beta1/model/transmuter_msgs.proto\x12\x1cosmosis.cosmwasmpool.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x1ecosmos/base/v1beta1/coin.proto"\x0e\n\x0cEmptyRequest"`\n\x19JoinPoolExecuteMsgRequest\x12C\n\tjoin_pool\x18\x01 \x01(\x0b2*.osmosis.cosmwasmpool.v1beta1.EmptyRequestB\x04\xc8\xde\x1f\x00"\x1c\n\x1aJoinPoolExecuteMsgResponse"`\n\x19ExitPoolExecuteMsgRequest\x12C\n\texit_pool\x18\x01 \x01(\x0b2*.osmosis.cosmwasmpool.v1beta1.EmptyRequestB\x04\xc8\xde\x1f\x00"\x1c\n\x1aExitPoolExecuteMsgResponseBLZJgithub.com/osmosis-labs/osmosis/v21/x/cosmwasmpool/cosmwasm/msg/transmuterb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.cosmwasmpool.v1beta1.model.transmuter_msgs_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'ZJgithub.com/osmosis-labs/osmosis/v21/x/cosmwasmpool/cosmwasm/msg/transmuter'
    _JOINPOOLEXECUTEMSGREQUEST.fields_by_name['join_pool']._options = None
    _JOINPOOLEXECUTEMSGREQUEST.fields_by_name['join_pool']._serialized_options = b'\xc8\xde\x1f\x00'
    _EXITPOOLEXECUTEMSGREQUEST.fields_by_name['exit_pool']._options = None
    _EXITPOOLEXECUTEMSGREQUEST.fields_by_name['exit_pool']._serialized_options = b'\xc8\xde\x1f\x00'
    _globals['_EMPTYREQUEST']._serialized_start = 144
    _globals['_EMPTYREQUEST']._serialized_end = 158
    _globals['_JOINPOOLEXECUTEMSGREQUEST']._serialized_start = 160
    _globals['_JOINPOOLEXECUTEMSGREQUEST']._serialized_end = 256
    _globals['_JOINPOOLEXECUTEMSGRESPONSE']._serialized_start = 258
    _globals['_JOINPOOLEXECUTEMSGRESPONSE']._serialized_end = 286
    _globals['_EXITPOOLEXECUTEMSGREQUEST']._serialized_start = 288
    _globals['_EXITPOOLEXECUTEMSGREQUEST']._serialized_end = 384
    _globals['_EXITPOOLEXECUTEMSGRESPONSE']._serialized_start = 386
    _globals['_EXITPOOLEXECUTEMSGRESPONSE']._serialized_end = 414