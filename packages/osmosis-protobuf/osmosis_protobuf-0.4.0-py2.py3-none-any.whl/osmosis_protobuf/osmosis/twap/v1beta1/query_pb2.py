"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....osmosis.twap.v1beta1 import twap_record_pb2 as osmosis_dot_twap_dot_v1beta1_dot_twap__record__pb2
from ....osmosis.twap.v1beta1 import genesis_pb2 as osmosis_dot_twap_dot_v1beta1_dot_genesis__pb2
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from ....cosmos.base.query.v1beta1 import pagination_pb2 as cosmos_dot_base_dot_query_dot_v1beta1_dot_pagination__pb2
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n osmosis/twap/v1beta1/query.proto\x12\x14osmosis.twap.v1beta1\x1a\x14gogoproto/gogo.proto\x1a&osmosis/twap/v1beta1/twap_record.proto\x1a"osmosis/twap/v1beta1/genesis.proto\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a*cosmos/base/query/v1beta1/pagination.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x19google/protobuf/any.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x1fgoogle/protobuf/timestamp.proto"\xeb\x01\n\x15ArithmeticTwapRequest\x12\x0f\n\x07pool_id\x18\x01 \x01(\x04\x12\x12\n\nbase_asset\x18\x02 \x01(\t\x12\x13\n\x0bquote_asset\x18\x03 \x01(\t\x12M\n\nstart_time\x18\x04 \x01(\x0b2\x1a.google.protobuf.TimestampB\x1d\xc8\xde\x1f\x00\xf2\xde\x1f\x11yaml:"start_time"\x90\xdf\x1f\x01\x12I\n\x08end_time\x18\x05 \x01(\x0b2\x1a.google.protobuf.TimestampB\x1b\xc8\xde\x1f\x01\xf2\xde\x1f\x0fyaml:"end_time"\x90\xdf\x1f\x01"p\n\x16ArithmeticTwapResponse\x12V\n\x0farithmetic_twap\x18\x01 \x01(\tB=\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x16yaml:"arithmetic_twap""\xa5\x01\n\x1aArithmeticTwapToNowRequest\x12\x0f\n\x07pool_id\x18\x01 \x01(\x04\x12\x12\n\nbase_asset\x18\x02 \x01(\t\x12\x13\n\x0bquote_asset\x18\x03 \x01(\t\x12M\n\nstart_time\x18\x04 \x01(\x0b2\x1a.google.protobuf.TimestampB\x1d\xc8\xde\x1f\x00\xf2\xde\x1f\x11yaml:"start_time"\x90\xdf\x1f\x01"u\n\x1bArithmeticTwapToNowResponse\x12V\n\x0farithmetic_twap\x18\x01 \x01(\tB=\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x16yaml:"arithmetic_twap""\xea\x01\n\x14GeometricTwapRequest\x12\x0f\n\x07pool_id\x18\x01 \x01(\x04\x12\x12\n\nbase_asset\x18\x02 \x01(\t\x12\x13\n\x0bquote_asset\x18\x03 \x01(\t\x12M\n\nstart_time\x18\x04 \x01(\x0b2\x1a.google.protobuf.TimestampB\x1d\xc8\xde\x1f\x00\xf2\xde\x1f\x11yaml:"start_time"\x90\xdf\x1f\x01\x12I\n\x08end_time\x18\x05 \x01(\x0b2\x1a.google.protobuf.TimestampB\x1b\xc8\xde\x1f\x01\xf2\xde\x1f\x0fyaml:"end_time"\x90\xdf\x1f\x01"m\n\x15GeometricTwapResponse\x12T\n\x0egeometric_twap\x18\x01 \x01(\tB<\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x15yaml:"geometric_twap""\xa4\x01\n\x19GeometricTwapToNowRequest\x12\x0f\n\x07pool_id\x18\x01 \x01(\x04\x12\x12\n\nbase_asset\x18\x02 \x01(\t\x12\x13\n\x0bquote_asset\x18\x03 \x01(\t\x12M\n\nstart_time\x18\x04 \x01(\x0b2\x1a.google.protobuf.TimestampB\x1d\xc8\xde\x1f\x00\xf2\xde\x1f\x11yaml:"start_time"\x90\xdf\x1f\x01"r\n\x1aGeometricTwapToNowResponse\x12T\n\x0egeometric_twap\x18\x01 \x01(\tB<\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x15yaml:"geometric_twap""\x0f\n\rParamsRequest"D\n\x0eParamsResponse\x122\n\x06params\x18\x01 \x01(\x0b2\x1c.osmosis.twap.v1beta1.ParamsB\x04\xc8\xde\x1f\x002\x92\x06\n\x05Query\x12y\n\x06Params\x12#.osmosis.twap.v1beta1.ParamsRequest\x1a$.osmosis.twap.v1beta1.ParamsResponse"$\x82\xd3\xe4\x93\x02\x1e\x12\x1c/osmosis/twap/v1beta1/Params\x12\x99\x01\n\x0eArithmeticTwap\x12+.osmosis.twap.v1beta1.ArithmeticTwapRequest\x1a,.osmosis.twap.v1beta1.ArithmeticTwapResponse",\x82\xd3\xe4\x93\x02&\x12$/osmosis/twap/v1beta1/ArithmeticTwap\x12\xad\x01\n\x13ArithmeticTwapToNow\x120.osmosis.twap.v1beta1.ArithmeticTwapToNowRequest\x1a1.osmosis.twap.v1beta1.ArithmeticTwapToNowResponse"1\x82\xd3\xe4\x93\x02+\x12)/osmosis/twap/v1beta1/ArithmeticTwapToNow\x12\x95\x01\n\rGeometricTwap\x12*.osmosis.twap.v1beta1.GeometricTwapRequest\x1a+.osmosis.twap.v1beta1.GeometricTwapResponse"+\x82\xd3\xe4\x93\x02%\x12#/osmosis/twap/v1beta1/GeometricTwap\x12\xa9\x01\n\x12GeometricTwapToNow\x12/.osmosis.twap.v1beta1.GeometricTwapToNowRequest\x1a0.osmosis.twap.v1beta1.GeometricTwapToNowResponse"0\x82\xd3\xe4\x93\x02*\x12(/osmosis/twap/v1beta1/GeometricTwapToNowB>Z<github.com/osmosis-labs/osmosis/v21/x/twap/client/queryprotob\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.twap.v1beta1.query_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z<github.com/osmosis-labs/osmosis/v21/x/twap/client/queryproto'
    _ARITHMETICTWAPREQUEST.fields_by_name['start_time']._options = None
    _ARITHMETICTWAPREQUEST.fields_by_name['start_time']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x11yaml:"start_time"\x90\xdf\x1f\x01'
    _ARITHMETICTWAPREQUEST.fields_by_name['end_time']._options = None
    _ARITHMETICTWAPREQUEST.fields_by_name['end_time']._serialized_options = b'\xc8\xde\x1f\x01\xf2\xde\x1f\x0fyaml:"end_time"\x90\xdf\x1f\x01'
    _ARITHMETICTWAPRESPONSE.fields_by_name['arithmetic_twap']._options = None
    _ARITHMETICTWAPRESPONSE.fields_by_name['arithmetic_twap']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x16yaml:"arithmetic_twap"'
    _ARITHMETICTWAPTONOWREQUEST.fields_by_name['start_time']._options = None
    _ARITHMETICTWAPTONOWREQUEST.fields_by_name['start_time']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x11yaml:"start_time"\x90\xdf\x1f\x01'
    _ARITHMETICTWAPTONOWRESPONSE.fields_by_name['arithmetic_twap']._options = None
    _ARITHMETICTWAPTONOWRESPONSE.fields_by_name['arithmetic_twap']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x16yaml:"arithmetic_twap"'
    _GEOMETRICTWAPREQUEST.fields_by_name['start_time']._options = None
    _GEOMETRICTWAPREQUEST.fields_by_name['start_time']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x11yaml:"start_time"\x90\xdf\x1f\x01'
    _GEOMETRICTWAPREQUEST.fields_by_name['end_time']._options = None
    _GEOMETRICTWAPREQUEST.fields_by_name['end_time']._serialized_options = b'\xc8\xde\x1f\x01\xf2\xde\x1f\x0fyaml:"end_time"\x90\xdf\x1f\x01'
    _GEOMETRICTWAPRESPONSE.fields_by_name['geometric_twap']._options = None
    _GEOMETRICTWAPRESPONSE.fields_by_name['geometric_twap']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x15yaml:"geometric_twap"'
    _GEOMETRICTWAPTONOWREQUEST.fields_by_name['start_time']._options = None
    _GEOMETRICTWAPTONOWREQUEST.fields_by_name['start_time']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x11yaml:"start_time"\x90\xdf\x1f\x01'
    _GEOMETRICTWAPTONOWRESPONSE.fields_by_name['geometric_twap']._options = None
    _GEOMETRICTWAPTONOWRESPONSE.fields_by_name['geometric_twap']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x15yaml:"geometric_twap"'
    _PARAMSRESPONSE.fields_by_name['params']._options = None
    _PARAMSRESPONSE.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERY.methods_by_name['Params']._options = None
    _QUERY.methods_by_name['Params']._serialized_options = b'\x82\xd3\xe4\x93\x02\x1e\x12\x1c/osmosis/twap/v1beta1/Params'
    _QUERY.methods_by_name['ArithmeticTwap']._options = None
    _QUERY.methods_by_name['ArithmeticTwap']._serialized_options = b'\x82\xd3\xe4\x93\x02&\x12$/osmosis/twap/v1beta1/ArithmeticTwap'
    _QUERY.methods_by_name['ArithmeticTwapToNow']._options = None
    _QUERY.methods_by_name['ArithmeticTwapToNow']._serialized_options = b'\x82\xd3\xe4\x93\x02+\x12)/osmosis/twap/v1beta1/ArithmeticTwapToNow'
    _QUERY.methods_by_name['GeometricTwap']._options = None
    _QUERY.methods_by_name['GeometricTwap']._serialized_options = b'\x82\xd3\xe4\x93\x02%\x12#/osmosis/twap/v1beta1/GeometricTwap'
    _QUERY.methods_by_name['GeometricTwapToNow']._options = None
    _QUERY.methods_by_name['GeometricTwapToNow']._serialized_options = b'\x82\xd3\xe4\x93\x02*\x12(/osmosis/twap/v1beta1/GeometricTwapToNow'
    _globals['_ARITHMETICTWAPREQUEST']._serialized_start = 350
    _globals['_ARITHMETICTWAPREQUEST']._serialized_end = 585
    _globals['_ARITHMETICTWAPRESPONSE']._serialized_start = 587
    _globals['_ARITHMETICTWAPRESPONSE']._serialized_end = 699
    _globals['_ARITHMETICTWAPTONOWREQUEST']._serialized_start = 702
    _globals['_ARITHMETICTWAPTONOWREQUEST']._serialized_end = 867
    _globals['_ARITHMETICTWAPTONOWRESPONSE']._serialized_start = 869
    _globals['_ARITHMETICTWAPTONOWRESPONSE']._serialized_end = 986
    _globals['_GEOMETRICTWAPREQUEST']._serialized_start = 989
    _globals['_GEOMETRICTWAPREQUEST']._serialized_end = 1223
    _globals['_GEOMETRICTWAPRESPONSE']._serialized_start = 1225
    _globals['_GEOMETRICTWAPRESPONSE']._serialized_end = 1334
    _globals['_GEOMETRICTWAPTONOWREQUEST']._serialized_start = 1337
    _globals['_GEOMETRICTWAPTONOWREQUEST']._serialized_end = 1501
    _globals['_GEOMETRICTWAPTONOWRESPONSE']._serialized_start = 1503
    _globals['_GEOMETRICTWAPTONOWRESPONSE']._serialized_end = 1617
    _globals['_PARAMSREQUEST']._serialized_start = 1619
    _globals['_PARAMSREQUEST']._serialized_end = 1634
    _globals['_PARAMSRESPONSE']._serialized_start = 1636
    _globals['_PARAMSRESPONSE']._serialized_end = 1704
    _globals['_QUERY']._serialized_start = 1707
    _globals['_QUERY']._serialized_end = 2493