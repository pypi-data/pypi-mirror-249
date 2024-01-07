"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....osmosis.tokenfactory.v1beta1 import authorityMetadata_pb2 as osmosis_dot_tokenfactory_dot_v1beta1_dot_authorityMetadata__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n)osmosis/tokenfactory/v1beta1/params.proto\x12\x1cosmosis.tokenfactory.v1beta1\x1a\x14gogoproto/gogo.proto\x1a4osmosis/tokenfactory/v1beta1/authorityMetadata.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x1ecosmos/base/v1beta1/coin.proto"\xde\x01\n\x06Params\x12\x84\x01\n\x12denom_creation_fee\x18\x01 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinBM\xc8\xde\x1f\x00\xf2\xde\x1f\x19yaml:"denom_creation_fee"\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x12M\n\x1adenom_creation_gas_consume\x18\x02 \x01(\x04B)\xc8\xde\x1f\x01\xf2\xde\x1f!yaml:"denom_creation_gas_consume"B:Z8github.com/osmosis-labs/osmosis/v21/x/tokenfactory/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.tokenfactory.v1beta1.params_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z8github.com/osmosis-labs/osmosis/v21/x/tokenfactory/types'
    _PARAMS.fields_by_name['denom_creation_fee']._options = None
    _PARAMS.fields_by_name['denom_creation_fee']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x19yaml:"denom_creation_fee"\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _PARAMS.fields_by_name['denom_creation_gas_consume']._options = None
    _PARAMS.fields_by_name['denom_creation_gas_consume']._serialized_options = b'\xc8\xde\x1f\x01\xf2\xde\x1f!yaml:"denom_creation_gas_consume"'
    _globals['_PARAMS']._serialized_start = 211
    _globals['_PARAMS']._serialized_end = 433