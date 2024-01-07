"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from ....amino import amino_pb2 as amino_dot_amino__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1ecosmos/base/v1beta1/coin.proto\x12\x13cosmos.base.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x11amino/amino.proto"K\n\x04Coin\x12\r\n\x05denom\x18\x01 \x01(\t\x12.\n\x06amount\x18\x02 \x01(\tB\x1e\xc8\xde\x1f\x00\xda\xde\x1f\x03Int\xd2\xb4-\ncosmos.Int\xa8\xe7\xb0*\x01:\x04\xe8\xa0\x1f\x01"I\n\x07DecCoin\x12\r\n\x05denom\x18\x01 \x01(\t\x12)\n\x06amount\x18\x02 \x01(\tB\x19\xc8\xde\x1f\x00\xda\xde\x1f\x03Dec\xd2\xb4-\ncosmos.Dec:\x04\xe8\xa0\x1f\x01"2\n\x08IntProto\x12&\n\x03int\x18\x01 \x01(\tB\x19\xc8\xde\x1f\x00\xda\xde\x1f\x03Int\xd2\xb4-\ncosmos.Int"2\n\x08DecProto\x12&\n\x03dec\x18\x01 \x01(\tB\x19\xc8\xde\x1f\x00\xda\xde\x1f\x03Dec\xd2\xb4-\ncosmos.DecB,Z"github.com/cosmos/cosmos-sdk/types\xd8\xe1\x1e\x00\x80\xe2\x1e\x00b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.base.v1beta1.coin_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z"github.com/cosmos/cosmos-sdk/types\xd8\xe1\x1e\x00\x80\xe2\x1e\x00'
    _COIN.fields_by_name['amount']._options = None
    _COIN.fields_by_name['amount']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x03Int\xd2\xb4-\ncosmos.Int\xa8\xe7\xb0*\x01'
    _COIN._options = None
    _COIN._serialized_options = b'\xe8\xa0\x1f\x01'
    _DECCOIN.fields_by_name['amount']._options = None
    _DECCOIN.fields_by_name['amount']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x03Dec\xd2\xb4-\ncosmos.Dec'
    _DECCOIN._options = None
    _DECCOIN._serialized_options = b'\xe8\xa0\x1f\x01'
    _INTPROTO.fields_by_name['int']._options = None
    _INTPROTO.fields_by_name['int']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x03Int\xd2\xb4-\ncosmos.Int'
    _DECPROTO.fields_by_name['dec']._options = None
    _DECPROTO.fields_by_name['dec']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x03Dec\xd2\xb4-\ncosmos.Dec'
    _globals['_COIN']._serialized_start = 123
    _globals['_COIN']._serialized_end = 198
    _globals['_DECCOIN']._serialized_start = 200
    _globals['_DECCOIN']._serialized_end = 273
    _globals['_INTPROTO']._serialized_start = 275
    _globals['_INTPROTO']._serialized_end = 325
    _globals['_DECPROTO']._serialized_start = 327
    _globals['_DECPROTO']._serialized_end = 377