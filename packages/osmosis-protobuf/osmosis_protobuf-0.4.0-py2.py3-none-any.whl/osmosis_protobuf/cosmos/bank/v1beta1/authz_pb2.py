"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....amino import amino_pb2 as amino_dot_amino__pb2
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fcosmos/bank/v1beta1/authz.proto\x12\x13cosmos.bank.v1beta1\x1a\x11amino/amino.proto\x1a\x14gogoproto/gogo.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x1ecosmos/base/v1beta1/coin.proto"\xf1\x01\n\x11SendAuthorization\x12e\n\x0bspend_limit\x18\x01 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB5\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xa8\xe7\xb0*\x01\x12,\n\nallow_list\x18\x02 \x03(\tB\x18\xd2\xb4-\x14cosmos.AddressString:G\xca\xb4-"cosmos.authz.v1beta1.Authorization\x8a\xe7\xb0*\x1ccosmos-sdk/SendAuthorizationB+Z)github.com/cosmos/cosmos-sdk/x/bank/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.bank.v1beta1.authz_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z)github.com/cosmos/cosmos-sdk/x/bank/types'
    _SENDAUTHORIZATION.fields_by_name['spend_limit']._options = None
    _SENDAUTHORIZATION.fields_by_name['spend_limit']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xa8\xe7\xb0*\x01'
    _SENDAUTHORIZATION.fields_by_name['allow_list']._options = None
    _SENDAUTHORIZATION.fields_by_name['allow_list']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _SENDAUTHORIZATION._options = None
    _SENDAUTHORIZATION._serialized_options = b'\xca\xb4-"cosmos.authz.v1beta1.Authorization\x8a\xe7\xb0*\x1ccosmos-sdk/SendAuthorization'
    _globals['_SENDAUTHORIZATION']._serialized_start = 157
    _globals['_SENDAUTHORIZATION']._serialized_end = 398