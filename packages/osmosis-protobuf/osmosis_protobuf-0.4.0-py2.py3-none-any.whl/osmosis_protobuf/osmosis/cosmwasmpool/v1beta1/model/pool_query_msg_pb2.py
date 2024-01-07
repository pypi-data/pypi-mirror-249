"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from .....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from .....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n7osmosis/cosmwasmpool/v1beta1/model/pool_query_msg.proto\x12\x1cosmosis.cosmwasmpool.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x1ecosmos/base/v1beta1/coin.proto"[\n\x12GetSwapFeeQueryMsg\x12E\n\x0cget_swap_fee\x18\x01 \x01(\x0b2).osmosis.cosmwasmpool.v1beta1.EmptyStructB\x04\xc8\xde\x1f\x00"S\n\x1aGetSwapFeeQueryMsgResponse\x125\n\x08swap_fee\x18\x03 \x01(\tB#\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec"@\n\tSpotPrice\x12\x19\n\x11quote_asset_denom\x18\x01 \x01(\t\x12\x18\n\x10base_asset_denom\x18\x02 \x01(\t"V\n\x11SpotPriceQueryMsg\x12A\n\nspot_price\x18\x01 \x01(\x0b2\'.osmosis.cosmwasmpool.v1beta1.SpotPriceB\x04\xc8\xde\x1f\x00"/\n\x19SpotPriceQueryMsgResponse\x12\x12\n\nspot_price\x18\x01 \x01(\t"\r\n\x0bEmptyStruct"r\n\x1dGetTotalPoolLiquidityQueryMsg\x12Q\n\x18get_total_pool_liquidity\x18\x01 \x01(\x0b2).osmosis.cosmwasmpool.v1beta1.EmptyStructB\x04\xc8\xde\x1f\x00"f\n%GetTotalPoolLiquidityQueryMsgResponse\x12=\n\x14total_pool_liquidity\x18\x01 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB\x04\xc8\xde\x1f\x00"c\n\x16GetTotalSharesQueryMsg\x12I\n\x10get_total_shares\x18\x01 \x01(\x0b2).osmosis.cosmwasmpool.v1beta1.EmptyStructB\x04\xc8\xde\x1f\x00"6\n\x1eGetTotalSharesQueryMsgResponse\x12\x14\n\x0ctotal_shares\x18\x01 \x01(\tBAZ?github.com/osmosis-labs/osmosis/v21/x/cosmwasmpool/cosmwasm/msgb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.cosmwasmpool.v1beta1.model.pool_query_msg_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z?github.com/osmosis-labs/osmosis/v21/x/cosmwasmpool/cosmwasm/msg'
    _GETSWAPFEEQUERYMSG.fields_by_name['get_swap_fee']._options = None
    _GETSWAPFEEQUERYMSG.fields_by_name['get_swap_fee']._serialized_options = b'\xc8\xde\x1f\x00'
    _GETSWAPFEEQUERYMSGRESPONSE.fields_by_name['swap_fee']._options = None
    _GETSWAPFEEQUERYMSGRESPONSE.fields_by_name['swap_fee']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec'
    _SPOTPRICEQUERYMSG.fields_by_name['spot_price']._options = None
    _SPOTPRICEQUERYMSG.fields_by_name['spot_price']._serialized_options = b'\xc8\xde\x1f\x00'
    _GETTOTALPOOLLIQUIDITYQUERYMSG.fields_by_name['get_total_pool_liquidity']._options = None
    _GETTOTALPOOLLIQUIDITYQUERYMSG.fields_by_name['get_total_pool_liquidity']._serialized_options = b'\xc8\xde\x1f\x00'
    _GETTOTALPOOLLIQUIDITYQUERYMSGRESPONSE.fields_by_name['total_pool_liquidity']._options = None
    _GETTOTALPOOLLIQUIDITYQUERYMSGRESPONSE.fields_by_name['total_pool_liquidity']._serialized_options = b'\xc8\xde\x1f\x00'
    _GETTOTALSHARESQUERYMSG.fields_by_name['get_total_shares']._options = None
    _GETTOTALSHARESQUERYMSG.fields_by_name['get_total_shares']._serialized_options = b'\xc8\xde\x1f\x00'
    _globals['_GETSWAPFEEQUERYMSG']._serialized_start = 143
    _globals['_GETSWAPFEEQUERYMSG']._serialized_end = 234
    _globals['_GETSWAPFEEQUERYMSGRESPONSE']._serialized_start = 236
    _globals['_GETSWAPFEEQUERYMSGRESPONSE']._serialized_end = 319
    _globals['_SPOTPRICE']._serialized_start = 321
    _globals['_SPOTPRICE']._serialized_end = 385
    _globals['_SPOTPRICEQUERYMSG']._serialized_start = 387
    _globals['_SPOTPRICEQUERYMSG']._serialized_end = 473
    _globals['_SPOTPRICEQUERYMSGRESPONSE']._serialized_start = 475
    _globals['_SPOTPRICEQUERYMSGRESPONSE']._serialized_end = 522
    _globals['_EMPTYSTRUCT']._serialized_start = 524
    _globals['_EMPTYSTRUCT']._serialized_end = 537
    _globals['_GETTOTALPOOLLIQUIDITYQUERYMSG']._serialized_start = 539
    _globals['_GETTOTALPOOLLIQUIDITYQUERYMSG']._serialized_end = 653
    _globals['_GETTOTALPOOLLIQUIDITYQUERYMSGRESPONSE']._serialized_start = 655
    _globals['_GETTOTALPOOLLIQUIDITYQUERYMSGRESPONSE']._serialized_end = 757
    _globals['_GETTOTALSHARESQUERYMSG']._serialized_start = 759
    _globals['_GETTOTALSHARESQUERYMSG']._serialized_end = 858
    _globals['_GETTOTALSHARESQUERYMSGRESPONSE']._serialized_start = 860
    _globals['_GETTOTALSHARESQUERYMSGRESPONSE']._serialized_end = 914