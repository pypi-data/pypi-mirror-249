"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n,osmosis/poolmanager/v1beta1/swap_route.proto\x12\x1bosmosis.poolmanager.v1beta1\x1a\x14gogoproto/gogo.proto"m\n\x11SwapAmountInRoute\x12#\n\x07pool_id\x18\x01 \x01(\x04B\x12\xf2\xde\x1f\x0eyaml:"pool_id"\x123\n\x0ftoken_out_denom\x18\x02 \x01(\tB\x1a\xf2\xde\x1f\x16yaml:"token_out_denom""l\n\x12SwapAmountOutRoute\x12#\n\x07pool_id\x18\x01 \x01(\x04B\x12\xf2\xde\x1f\x0eyaml:"pool_id"\x121\n\x0etoken_in_denom\x18\x02 \x01(\tB\x19\xf2\xde\x1f\x15yaml:"token_in_denom""\xbf\x01\n\x16SwapAmountInSplitRoute\x12S\n\x05pools\x18\x01 \x03(\x0b2..osmosis.poolmanager.v1beta1.SwapAmountInRouteB\x14\xc8\xde\x1f\x00\xf2\xde\x1f\x0cyaml:"pools"\x12P\n\x0ftoken_in_amount\x18\x02 \x01(\tB7\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x16yaml:"token_in_amount""\xc3\x01\n\x17SwapAmountOutSplitRoute\x12T\n\x05pools\x18\x01 \x03(\x0b2/.osmosis.poolmanager.v1beta1.SwapAmountOutRouteB\x14\xc8\xde\x1f\x00\xf2\xde\x1f\x0cyaml:"pools"\x12R\n\x10token_out_amount\x18\x02 \x01(\tB8\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x17yaml:"token_out_amount"B9Z7github.com/osmosis-labs/osmosis/v21/x/poolmanager/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.poolmanager.v1beta1.swap_route_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z7github.com/osmosis-labs/osmosis/v21/x/poolmanager/types'
    _SWAPAMOUNTINROUTE.fields_by_name['pool_id']._options = None
    _SWAPAMOUNTINROUTE.fields_by_name['pool_id']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"pool_id"'
    _SWAPAMOUNTINROUTE.fields_by_name['token_out_denom']._options = None
    _SWAPAMOUNTINROUTE.fields_by_name['token_out_denom']._serialized_options = b'\xf2\xde\x1f\x16yaml:"token_out_denom"'
    _SWAPAMOUNTOUTROUTE.fields_by_name['pool_id']._options = None
    _SWAPAMOUNTOUTROUTE.fields_by_name['pool_id']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"pool_id"'
    _SWAPAMOUNTOUTROUTE.fields_by_name['token_in_denom']._options = None
    _SWAPAMOUNTOUTROUTE.fields_by_name['token_in_denom']._serialized_options = b'\xf2\xde\x1f\x15yaml:"token_in_denom"'
    _SWAPAMOUNTINSPLITROUTE.fields_by_name['pools']._options = None
    _SWAPAMOUNTINSPLITROUTE.fields_by_name['pools']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x0cyaml:"pools"'
    _SWAPAMOUNTINSPLITROUTE.fields_by_name['token_in_amount']._options = None
    _SWAPAMOUNTINSPLITROUTE.fields_by_name['token_in_amount']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x16yaml:"token_in_amount"'
    _SWAPAMOUNTOUTSPLITROUTE.fields_by_name['pools']._options = None
    _SWAPAMOUNTOUTSPLITROUTE.fields_by_name['pools']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x0cyaml:"pools"'
    _SWAPAMOUNTOUTSPLITROUTE.fields_by_name['token_out_amount']._options = None
    _SWAPAMOUNTOUTSPLITROUTE.fields_by_name['token_out_amount']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x17yaml:"token_out_amount"'
    _globals['_SWAPAMOUNTINROUTE']._serialized_start = 99
    _globals['_SWAPAMOUNTINROUTE']._serialized_end = 208
    _globals['_SWAPAMOUNTOUTROUTE']._serialized_start = 210
    _globals['_SWAPAMOUNTOUTROUTE']._serialized_end = 318
    _globals['_SWAPAMOUNTINSPLITROUTE']._serialized_start = 321
    _globals['_SWAPAMOUNTINSPLITROUTE']._serialized_end = 512
    _globals['_SWAPAMOUNTOUTSPLITROUTE']._serialized_start = 515
    _globals['_SWAPAMOUNTOUTSPLITROUTE']._serialized_end = 710