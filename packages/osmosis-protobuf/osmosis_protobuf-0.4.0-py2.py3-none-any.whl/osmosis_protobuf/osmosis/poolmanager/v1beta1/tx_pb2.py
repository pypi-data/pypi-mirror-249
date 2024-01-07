"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....amino import amino_pb2 as amino_dot_amino__pb2
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from ....osmosis.poolmanager.v1beta1 import swap_route_pb2 as osmosis_dot_poolmanager_dot_v1beta1_dot_swap__route__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$osmosis/poolmanager/v1beta1/tx.proto\x12\x1bosmosis.poolmanager.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x11amino/amino.proto\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a,osmosis/poolmanager/v1beta1/swap_route.proto"\xd0\x02\n\x14MsgSwapExactAmountIn\x12!\n\x06sender\x18\x01 \x01(\tB\x11\xf2\xde\x1f\ryaml:"sender"\x12D\n\x06routes\x18\x02 \x03(\x0b2..osmosis.poolmanager.v1beta1.SwapAmountInRouteB\x04\xc8\xde\x1f\x00\x12D\n\x08token_in\x18\x03 \x01(\x0b2\x19.cosmos.base.v1beta1.CoinB\x17\xc8\xde\x1f\x00\xf2\xde\x1f\x0fyaml:"token_in"\x12Z\n\x14token_out_min_amount\x18\x04 \x01(\tB<\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x1byaml:"token_out_min_amount":-\x8a\xe7\xb0*(osmosis/poolmanager/swap-exact-amount-in"r\n\x1cMsgSwapExactAmountInResponse\x12R\n\x10token_out_amount\x18\x01 \x01(\tB8\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x17yaml:"token_out_amount""\xc7\x02\n\x1eMsgSplitRouteSwapExactAmountIn\x12!\n\x06sender\x18\x01 \x01(\tB\x11\xf2\xde\x1f\ryaml:"sender"\x12I\n\x06routes\x18\x02 \x03(\x0b23.osmosis.poolmanager.v1beta1.SwapAmountInSplitRouteB\x04\xc8\xde\x1f\x00\x121\n\x0etoken_in_denom\x18\x03 \x01(\tB\x19\xf2\xde\x1f\x15yaml:"token_in_denom"\x12Z\n\x14token_out_min_amount\x18\x04 \x01(\tB<\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x1byaml:"token_out_min_amount":(\x8a\xe7\xb0*#osmosis/poolmanager/split-amount-in"|\n&MsgSplitRouteSwapExactAmountInResponse\x12R\n\x10token_out_amount\x18\x01 \x01(\tB8\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x17yaml:"token_out_amount""\xd3\x02\n\x15MsgSwapExactAmountOut\x12!\n\x06sender\x18\x01 \x01(\tB\x11\xf2\xde\x1f\ryaml:"sender"\x12E\n\x06routes\x18\x02 \x03(\x0b2/.osmosis.poolmanager.v1beta1.SwapAmountOutRouteB\x04\xc8\xde\x1f\x00\x12X\n\x13token_in_max_amount\x18\x03 \x01(\tB;\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x1ayaml:"token_in_max_amount"\x12F\n\ttoken_out\x18\x04 \x01(\x0b2\x19.cosmos.base.v1beta1.CoinB\x18\xc8\xde\x1f\x00\xf2\xde\x1f\x10yaml:"token_out":.\x8a\xe7\xb0*)osmosis/poolmanager/swap-exact-amount-out"q\n\x1dMsgSwapExactAmountOutResponse\x12P\n\x0ftoken_in_amount\x18\x01 \x01(\tB7\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x16yaml:"token_in_amount""\xca\x02\n\x1fMsgSplitRouteSwapExactAmountOut\x12!\n\x06sender\x18\x01 \x01(\tB\x11\xf2\xde\x1f\ryaml:"sender"\x12J\n\x06routes\x18\x02 \x03(\x0b24.osmosis.poolmanager.v1beta1.SwapAmountOutSplitRouteB\x04\xc8\xde\x1f\x00\x123\n\x0ftoken_out_denom\x18\x03 \x01(\tB\x1a\xf2\xde\x1f\x16yaml:"token_out_denom"\x12X\n\x13token_in_max_amount\x18\x04 \x01(\tB;\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x1ayaml:"token_in_max_amount":)\x8a\xe7\xb0*$osmosis/poolmanager/split-amount-out"{\n\'MsgSplitRouteSwapExactAmountOutResponse\x12P\n\x0ftoken_in_amount\x18\x01 \x01(\tB7\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x16yaml:"token_in_amount""\xe2\x01\n\x17MsgSetDenomPairTakerFee\x12!\n\x06sender\x18\x01 \x01(\tB\x11\xf2\xde\x1f\ryaml:"sender"\x12q\n\x14denom_pair_taker_fee\x18\x02 \x03(\x0b2..osmosis.poolmanager.v1beta1.DenomPairTakerFeeB#\xc8\xde\x1f\x00\xf2\xde\x1f\x1byaml:"denom_pair_taker_fee":1\x8a\xe7\xb0*,osmosis/poolmanager/set-denom-pair-taker-fee"2\n\x1fMsgSetDenomPairTakerFeeResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08"\xa5\x01\n\x11DenomPairTakerFee\x12!\n\x06denom0\x18\x01 \x01(\tB\x11\xf2\xde\x1f\ryaml:"denom0"\x12!\n\x06denom1\x18\x02 \x01(\tB\x11\xf2\xde\x1f\ryaml:"denom1"\x12J\n\ttaker_fee\x18\x03 \x01(\tB7\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x10yaml:"taker_fee"2\xe4\x05\n\x03Msg\x12\x81\x01\n\x11SwapExactAmountIn\x121.osmosis.poolmanager.v1beta1.MsgSwapExactAmountIn\x1a9.osmosis.poolmanager.v1beta1.MsgSwapExactAmountInResponse\x12\x84\x01\n\x12SwapExactAmountOut\x122.osmosis.poolmanager.v1beta1.MsgSwapExactAmountOut\x1a:.osmosis.poolmanager.v1beta1.MsgSwapExactAmountOutResponse\x12\x9f\x01\n\x1bSplitRouteSwapExactAmountIn\x12;.osmosis.poolmanager.v1beta1.MsgSplitRouteSwapExactAmountIn\x1aC.osmosis.poolmanager.v1beta1.MsgSplitRouteSwapExactAmountInResponse\x12\xa2\x01\n\x1cSplitRouteSwapExactAmountOut\x12<.osmosis.poolmanager.v1beta1.MsgSplitRouteSwapExactAmountOut\x1aD.osmosis.poolmanager.v1beta1.MsgSplitRouteSwapExactAmountOutResponse\x12\x8a\x01\n\x14SetDenomPairTakerFee\x124.osmosis.poolmanager.v1beta1.MsgSetDenomPairTakerFee\x1a<.osmosis.poolmanager.v1beta1.MsgSetDenomPairTakerFeeResponseB9Z7github.com/osmosis-labs/osmosis/v21/x/poolmanager/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.poolmanager.v1beta1.tx_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z7github.com/osmosis-labs/osmosis/v21/x/poolmanager/types'
    _MSGSWAPEXACTAMOUNTIN.fields_by_name['sender']._options = None
    _MSGSWAPEXACTAMOUNTIN.fields_by_name['sender']._serialized_options = b'\xf2\xde\x1f\ryaml:"sender"'
    _MSGSWAPEXACTAMOUNTIN.fields_by_name['routes']._options = None
    _MSGSWAPEXACTAMOUNTIN.fields_by_name['routes']._serialized_options = b'\xc8\xde\x1f\x00'
    _MSGSWAPEXACTAMOUNTIN.fields_by_name['token_in']._options = None
    _MSGSWAPEXACTAMOUNTIN.fields_by_name['token_in']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x0fyaml:"token_in"'
    _MSGSWAPEXACTAMOUNTIN.fields_by_name['token_out_min_amount']._options = None
    _MSGSWAPEXACTAMOUNTIN.fields_by_name['token_out_min_amount']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x1byaml:"token_out_min_amount"'
    _MSGSWAPEXACTAMOUNTIN._options = None
    _MSGSWAPEXACTAMOUNTIN._serialized_options = b'\x8a\xe7\xb0*(osmosis/poolmanager/swap-exact-amount-in'
    _MSGSWAPEXACTAMOUNTINRESPONSE.fields_by_name['token_out_amount']._options = None
    _MSGSWAPEXACTAMOUNTINRESPONSE.fields_by_name['token_out_amount']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x17yaml:"token_out_amount"'
    _MSGSPLITROUTESWAPEXACTAMOUNTIN.fields_by_name['sender']._options = None
    _MSGSPLITROUTESWAPEXACTAMOUNTIN.fields_by_name['sender']._serialized_options = b'\xf2\xde\x1f\ryaml:"sender"'
    _MSGSPLITROUTESWAPEXACTAMOUNTIN.fields_by_name['routes']._options = None
    _MSGSPLITROUTESWAPEXACTAMOUNTIN.fields_by_name['routes']._serialized_options = b'\xc8\xde\x1f\x00'
    _MSGSPLITROUTESWAPEXACTAMOUNTIN.fields_by_name['token_in_denom']._options = None
    _MSGSPLITROUTESWAPEXACTAMOUNTIN.fields_by_name['token_in_denom']._serialized_options = b'\xf2\xde\x1f\x15yaml:"token_in_denom"'
    _MSGSPLITROUTESWAPEXACTAMOUNTIN.fields_by_name['token_out_min_amount']._options = None
    _MSGSPLITROUTESWAPEXACTAMOUNTIN.fields_by_name['token_out_min_amount']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x1byaml:"token_out_min_amount"'
    _MSGSPLITROUTESWAPEXACTAMOUNTIN._options = None
    _MSGSPLITROUTESWAPEXACTAMOUNTIN._serialized_options = b'\x8a\xe7\xb0*#osmosis/poolmanager/split-amount-in'
    _MSGSPLITROUTESWAPEXACTAMOUNTINRESPONSE.fields_by_name['token_out_amount']._options = None
    _MSGSPLITROUTESWAPEXACTAMOUNTINRESPONSE.fields_by_name['token_out_amount']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x17yaml:"token_out_amount"'
    _MSGSWAPEXACTAMOUNTOUT.fields_by_name['sender']._options = None
    _MSGSWAPEXACTAMOUNTOUT.fields_by_name['sender']._serialized_options = b'\xf2\xde\x1f\ryaml:"sender"'
    _MSGSWAPEXACTAMOUNTOUT.fields_by_name['routes']._options = None
    _MSGSWAPEXACTAMOUNTOUT.fields_by_name['routes']._serialized_options = b'\xc8\xde\x1f\x00'
    _MSGSWAPEXACTAMOUNTOUT.fields_by_name['token_in_max_amount']._options = None
    _MSGSWAPEXACTAMOUNTOUT.fields_by_name['token_in_max_amount']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x1ayaml:"token_in_max_amount"'
    _MSGSWAPEXACTAMOUNTOUT.fields_by_name['token_out']._options = None
    _MSGSWAPEXACTAMOUNTOUT.fields_by_name['token_out']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x10yaml:"token_out"'
    _MSGSWAPEXACTAMOUNTOUT._options = None
    _MSGSWAPEXACTAMOUNTOUT._serialized_options = b'\x8a\xe7\xb0*)osmosis/poolmanager/swap-exact-amount-out'
    _MSGSWAPEXACTAMOUNTOUTRESPONSE.fields_by_name['token_in_amount']._options = None
    _MSGSWAPEXACTAMOUNTOUTRESPONSE.fields_by_name['token_in_amount']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x16yaml:"token_in_amount"'
    _MSGSPLITROUTESWAPEXACTAMOUNTOUT.fields_by_name['sender']._options = None
    _MSGSPLITROUTESWAPEXACTAMOUNTOUT.fields_by_name['sender']._serialized_options = b'\xf2\xde\x1f\ryaml:"sender"'
    _MSGSPLITROUTESWAPEXACTAMOUNTOUT.fields_by_name['routes']._options = None
    _MSGSPLITROUTESWAPEXACTAMOUNTOUT.fields_by_name['routes']._serialized_options = b'\xc8\xde\x1f\x00'
    _MSGSPLITROUTESWAPEXACTAMOUNTOUT.fields_by_name['token_out_denom']._options = None
    _MSGSPLITROUTESWAPEXACTAMOUNTOUT.fields_by_name['token_out_denom']._serialized_options = b'\xf2\xde\x1f\x16yaml:"token_out_denom"'
    _MSGSPLITROUTESWAPEXACTAMOUNTOUT.fields_by_name['token_in_max_amount']._options = None
    _MSGSPLITROUTESWAPEXACTAMOUNTOUT.fields_by_name['token_in_max_amount']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x1ayaml:"token_in_max_amount"'
    _MSGSPLITROUTESWAPEXACTAMOUNTOUT._options = None
    _MSGSPLITROUTESWAPEXACTAMOUNTOUT._serialized_options = b'\x8a\xe7\xb0*$osmosis/poolmanager/split-amount-out'
    _MSGSPLITROUTESWAPEXACTAMOUNTOUTRESPONSE.fields_by_name['token_in_amount']._options = None
    _MSGSPLITROUTESWAPEXACTAMOUNTOUTRESPONSE.fields_by_name['token_in_amount']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x16yaml:"token_in_amount"'
    _MSGSETDENOMPAIRTAKERFEE.fields_by_name['sender']._options = None
    _MSGSETDENOMPAIRTAKERFEE.fields_by_name['sender']._serialized_options = b'\xf2\xde\x1f\ryaml:"sender"'
    _MSGSETDENOMPAIRTAKERFEE.fields_by_name['denom_pair_taker_fee']._options = None
    _MSGSETDENOMPAIRTAKERFEE.fields_by_name['denom_pair_taker_fee']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x1byaml:"denom_pair_taker_fee"'
    _MSGSETDENOMPAIRTAKERFEE._options = None
    _MSGSETDENOMPAIRTAKERFEE._serialized_options = b'\x8a\xe7\xb0*,osmosis/poolmanager/set-denom-pair-taker-fee'
    _DENOMPAIRTAKERFEE.fields_by_name['denom0']._options = None
    _DENOMPAIRTAKERFEE.fields_by_name['denom0']._serialized_options = b'\xf2\xde\x1f\ryaml:"denom0"'
    _DENOMPAIRTAKERFEE.fields_by_name['denom1']._options = None
    _DENOMPAIRTAKERFEE.fields_by_name['denom1']._serialized_options = b'\xf2\xde\x1f\ryaml:"denom1"'
    _DENOMPAIRTAKERFEE.fields_by_name['taker_fee']._options = None
    _DENOMPAIRTAKERFEE.fields_by_name['taker_fee']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x10yaml:"taker_fee"'
    _globals['_MSGSWAPEXACTAMOUNTIN']._serialized_start = 189
    _globals['_MSGSWAPEXACTAMOUNTIN']._serialized_end = 525
    _globals['_MSGSWAPEXACTAMOUNTINRESPONSE']._serialized_start = 527
    _globals['_MSGSWAPEXACTAMOUNTINRESPONSE']._serialized_end = 641
    _globals['_MSGSPLITROUTESWAPEXACTAMOUNTIN']._serialized_start = 644
    _globals['_MSGSPLITROUTESWAPEXACTAMOUNTIN']._serialized_end = 971
    _globals['_MSGSPLITROUTESWAPEXACTAMOUNTINRESPONSE']._serialized_start = 973
    _globals['_MSGSPLITROUTESWAPEXACTAMOUNTINRESPONSE']._serialized_end = 1097
    _globals['_MSGSWAPEXACTAMOUNTOUT']._serialized_start = 1100
    _globals['_MSGSWAPEXACTAMOUNTOUT']._serialized_end = 1439
    _globals['_MSGSWAPEXACTAMOUNTOUTRESPONSE']._serialized_start = 1441
    _globals['_MSGSWAPEXACTAMOUNTOUTRESPONSE']._serialized_end = 1554
    _globals['_MSGSPLITROUTESWAPEXACTAMOUNTOUT']._serialized_start = 1557
    _globals['_MSGSPLITROUTESWAPEXACTAMOUNTOUT']._serialized_end = 1887
    _globals['_MSGSPLITROUTESWAPEXACTAMOUNTOUTRESPONSE']._serialized_start = 1889
    _globals['_MSGSPLITROUTESWAPEXACTAMOUNTOUTRESPONSE']._serialized_end = 2012
    _globals['_MSGSETDENOMPAIRTAKERFEE']._serialized_start = 2015
    _globals['_MSGSETDENOMPAIRTAKERFEE']._serialized_end = 2241
    _globals['_MSGSETDENOMPAIRTAKERFEERESPONSE']._serialized_start = 2243
    _globals['_MSGSETDENOMPAIRTAKERFEERESPONSE']._serialized_end = 2293
    _globals['_DENOMPAIRTAKERFEE']._serialized_start = 2296
    _globals['_DENOMPAIRTAKERFEE']._serialized_end = 2461
    _globals['_MSG']._serialized_start = 2464
    _globals['_MSG']._serialized_end = 3204