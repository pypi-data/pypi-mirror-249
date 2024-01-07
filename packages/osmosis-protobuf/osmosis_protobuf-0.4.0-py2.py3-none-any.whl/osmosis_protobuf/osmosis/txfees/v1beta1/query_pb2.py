"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from ....osmosis.txfees.v1beta1 import feetoken_pb2 as osmosis_dot_txfees_dot_v1beta1_dot_feetoken__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n"osmosis/txfees/v1beta1/query.proto\x12\x16osmosis.txfees.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1egoogle/protobuf/duration.proto\x1a%osmosis/txfees/v1beta1/feetoken.proto"\x17\n\x15QueryFeeTokensRequest"i\n\x16QueryFeeTokensResponse\x12O\n\nfee_tokens\x18\x01 \x03(\x0b2 .osmosis.txfees.v1beta1.FeeTokenB\x19\xc8\xde\x1f\x00\xf2\xde\x1f\x11yaml:"fee_tokens""=\n\x1aQueryDenomSpotPriceRequest\x12\x1f\n\x05denom\x18\x01 \x01(\tB\x10\xf2\xde\x1f\x0cyaml:"denom""\x8f\x01\n\x1bQueryDenomSpotPriceResponse\x12"\n\x06poolID\x18\x01 \x01(\x04B\x12\xf2\xde\x1f\x0eyaml:"pool_id"\x12L\n\nspot_price\x18\x02 \x01(\tB8\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x11yaml:"spot_price"":\n\x17QueryDenomPoolIdRequest\x12\x1f\n\x05denom\x18\x01 \x01(\tB\x10\xf2\xde\x1f\x0cyaml:"denom"">\n\x18QueryDenomPoolIdResponse\x12"\n\x06poolID\x18\x01 \x01(\x04B\x12\xf2\xde\x1f\x0eyaml:"pool_id""\x17\n\x15QueryBaseDenomRequest"C\n\x16QueryBaseDenomResponse\x12)\n\nbase_denom\x18\x01 \x01(\tB\x15\xf2\xde\x1f\x11yaml:"base_denom""\x18\n\x16QueryEipBaseFeeRequest"c\n\x17QueryEipBaseFeeResponse\x12H\n\x08base_fee\x18\x01 \x01(\tB6\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x0fyaml:"base_fee"2\xb9\x06\n\x05Query\x12\x96\x01\n\tFeeTokens\x12-.osmosis.txfees.v1beta1.QueryFeeTokensRequest\x1a..osmosis.txfees.v1beta1.QueryFeeTokensResponse"*\x82\xd3\xe4\x93\x02$\x12"/osmosis/txfees/v1beta1/fee_tokens\x12\xae\x01\n\x0eDenomSpotPrice\x122.osmosis.txfees.v1beta1.QueryDenomSpotPriceRequest\x1a3.osmosis.txfees.v1beta1.QueryDenomSpotPriceResponse"3\x82\xd3\xe4\x93\x02-\x12+/osmosis/txfees/v1beta1/spot_price_by_denom\x12\xa7\x01\n\x0bDenomPoolId\x12/.osmosis.txfees.v1beta1.QueryDenomPoolIdRequest\x1a0.osmosis.txfees.v1beta1.QueryDenomPoolIdResponse"5\x82\xd3\xe4\x93\x02/\x12-/osmosis/txfees/v1beta1/denom_pool_id/{denom}\x12\x96\x01\n\tBaseDenom\x12-.osmosis.txfees.v1beta1.QueryBaseDenomRequest\x1a..osmosis.txfees.v1beta1.QueryBaseDenomResponse"*\x82\xd3\xe4\x93\x02$\x12"/osmosis/txfees/v1beta1/base_denom\x12\xa2\x01\n\rGetEipBaseFee\x12..osmosis.txfees.v1beta1.QueryEipBaseFeeRequest\x1a/.osmosis.txfees.v1beta1.QueryEipBaseFeeResponse"0\x82\xd3\xe4\x93\x02*\x12(/osmosis/txfees/v1beta1/cur_eip_base_feeB4Z2github.com/osmosis-labs/osmosis/v21/x/txfees/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.txfees.v1beta1.query_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z2github.com/osmosis-labs/osmosis/v21/x/txfees/types'
    _QUERYFEETOKENSRESPONSE.fields_by_name['fee_tokens']._options = None
    _QUERYFEETOKENSRESPONSE.fields_by_name['fee_tokens']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x11yaml:"fee_tokens"'
    _QUERYDENOMSPOTPRICEREQUEST.fields_by_name['denom']._options = None
    _QUERYDENOMSPOTPRICEREQUEST.fields_by_name['denom']._serialized_options = b'\xf2\xde\x1f\x0cyaml:"denom"'
    _QUERYDENOMSPOTPRICERESPONSE.fields_by_name['poolID']._options = None
    _QUERYDENOMSPOTPRICERESPONSE.fields_by_name['poolID']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"pool_id"'
    _QUERYDENOMSPOTPRICERESPONSE.fields_by_name['spot_price']._options = None
    _QUERYDENOMSPOTPRICERESPONSE.fields_by_name['spot_price']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x11yaml:"spot_price"'
    _QUERYDENOMPOOLIDREQUEST.fields_by_name['denom']._options = None
    _QUERYDENOMPOOLIDREQUEST.fields_by_name['denom']._serialized_options = b'\xf2\xde\x1f\x0cyaml:"denom"'
    _QUERYDENOMPOOLIDRESPONSE.fields_by_name['poolID']._options = None
    _QUERYDENOMPOOLIDRESPONSE.fields_by_name['poolID']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"pool_id"'
    _QUERYBASEDENOMRESPONSE.fields_by_name['base_denom']._options = None
    _QUERYBASEDENOMRESPONSE.fields_by_name['base_denom']._serialized_options = b'\xf2\xde\x1f\x11yaml:"base_denom"'
    _QUERYEIPBASEFEERESPONSE.fields_by_name['base_fee']._options = None
    _QUERYEIPBASEFEERESPONSE.fields_by_name['base_fee']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x0fyaml:"base_fee"'
    _QUERY.methods_by_name['FeeTokens']._options = None
    _QUERY.methods_by_name['FeeTokens']._serialized_options = b'\x82\xd3\xe4\x93\x02$\x12"/osmosis/txfees/v1beta1/fee_tokens'
    _QUERY.methods_by_name['DenomSpotPrice']._options = None
    _QUERY.methods_by_name['DenomSpotPrice']._serialized_options = b'\x82\xd3\xe4\x93\x02-\x12+/osmosis/txfees/v1beta1/spot_price_by_denom'
    _QUERY.methods_by_name['DenomPoolId']._options = None
    _QUERY.methods_by_name['DenomPoolId']._serialized_options = b'\x82\xd3\xe4\x93\x02/\x12-/osmosis/txfees/v1beta1/denom_pool_id/{denom}'
    _QUERY.methods_by_name['BaseDenom']._options = None
    _QUERY.methods_by_name['BaseDenom']._serialized_options = b'\x82\xd3\xe4\x93\x02$\x12"/osmosis/txfees/v1beta1/base_denom'
    _QUERY.methods_by_name['GetEipBaseFee']._options = None
    _QUERY.methods_by_name['GetEipBaseFee']._serialized_options = b'\x82\xd3\xe4\x93\x02*\x12(/osmosis/txfees/v1beta1/cur_eip_base_fee'
    _globals['_QUERYFEETOKENSREQUEST']._serialized_start = 185
    _globals['_QUERYFEETOKENSREQUEST']._serialized_end = 208
    _globals['_QUERYFEETOKENSRESPONSE']._serialized_start = 210
    _globals['_QUERYFEETOKENSRESPONSE']._serialized_end = 315
    _globals['_QUERYDENOMSPOTPRICEREQUEST']._serialized_start = 317
    _globals['_QUERYDENOMSPOTPRICEREQUEST']._serialized_end = 378
    _globals['_QUERYDENOMSPOTPRICERESPONSE']._serialized_start = 381
    _globals['_QUERYDENOMSPOTPRICERESPONSE']._serialized_end = 524
    _globals['_QUERYDENOMPOOLIDREQUEST']._serialized_start = 526
    _globals['_QUERYDENOMPOOLIDREQUEST']._serialized_end = 584
    _globals['_QUERYDENOMPOOLIDRESPONSE']._serialized_start = 586
    _globals['_QUERYDENOMPOOLIDRESPONSE']._serialized_end = 648
    _globals['_QUERYBASEDENOMREQUEST']._serialized_start = 650
    _globals['_QUERYBASEDENOMREQUEST']._serialized_end = 673
    _globals['_QUERYBASEDENOMRESPONSE']._serialized_start = 675
    _globals['_QUERYBASEDENOMRESPONSE']._serialized_end = 742
    _globals['_QUERYEIPBASEFEEREQUEST']._serialized_start = 744
    _globals['_QUERYEIPBASEFEEREQUEST']._serialized_end = 768
    _globals['_QUERYEIPBASEFEERESPONSE']._serialized_start = 770
    _globals['_QUERYEIPBASEFEERESPONSE']._serialized_end = 869
    _globals['_QUERY']._serialized_start = 872
    _globals['_QUERY']._serialized_end = 1697