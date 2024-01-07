"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from ....amino import amino_pb2 as amino_dot_amino__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&cosmos/slashing/v1beta1/slashing.proto\x12\x17cosmos.slashing.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x11amino/amino.proto"\xeb\x01\n\x14ValidatorSigningInfo\x12)\n\x07address\x18\x01 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString\x12\x14\n\x0cstart_height\x18\x02 \x01(\x03\x12\x14\n\x0cindex_offset\x18\x03 \x01(\x03\x12?\n\x0cjailed_until\x18\x04 \x01(\x0b2\x1a.google.protobuf.TimestampB\r\xc8\xde\x1f\x00\x90\xdf\x1f\x01\xa8\xe7\xb0*\x01\x12\x12\n\ntombstoned\x18\x05 \x01(\x08\x12\x1d\n\x15missed_blocks_counter\x18\x06 \x01(\x03:\x08\x98\xa0\x1f\x00\xe8\xa0\x1f\x01"\x96\x03\n\x06Params\x12\x1c\n\x14signed_blocks_window\x18\x01 \x01(\x03\x12R\n\x15min_signed_per_window\x18\x02 \x01(\x0cB3\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xa8\xe7\xb0*\x01\x12H\n\x16downtime_jail_duration\x18\x03 \x01(\x0b2\x19.google.protobuf.DurationB\r\xc8\xde\x1f\x00\x98\xdf\x1f\x01\xa8\xe7\xb0*\x01\x12W\n\x1aslash_fraction_double_sign\x18\x04 \x01(\x0cB3\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xa8\xe7\xb0*\x01\x12T\n\x17slash_fraction_downtime\x18\x05 \x01(\x0cB3\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xa8\xe7\xb0*\x01:!\x8a\xe7\xb0*\x1ccosmos-sdk/x/slashing/ParamsB3Z-github.com/cosmos/cosmos-sdk/x/slashing/types\xa8\xe2\x1e\x01b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.slashing.v1beta1.slashing_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z-github.com/cosmos/cosmos-sdk/x/slashing/types\xa8\xe2\x1e\x01'
    _VALIDATORSIGNINGINFO.fields_by_name['address']._options = None
    _VALIDATORSIGNINGINFO.fields_by_name['address']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _VALIDATORSIGNINGINFO.fields_by_name['jailed_until']._options = None
    _VALIDATORSIGNINGINFO.fields_by_name['jailed_until']._serialized_options = b'\xc8\xde\x1f\x00\x90\xdf\x1f\x01\xa8\xe7\xb0*\x01'
    _VALIDATORSIGNINGINFO._options = None
    _VALIDATORSIGNINGINFO._serialized_options = b'\x98\xa0\x1f\x00\xe8\xa0\x1f\x01'
    _PARAMS.fields_by_name['min_signed_per_window']._options = None
    _PARAMS.fields_by_name['min_signed_per_window']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xa8\xe7\xb0*\x01'
    _PARAMS.fields_by_name['downtime_jail_duration']._options = None
    _PARAMS.fields_by_name['downtime_jail_duration']._serialized_options = b'\xc8\xde\x1f\x00\x98\xdf\x1f\x01\xa8\xe7\xb0*\x01'
    _PARAMS.fields_by_name['slash_fraction_double_sign']._options = None
    _PARAMS.fields_by_name['slash_fraction_double_sign']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xa8\xe7\xb0*\x01'
    _PARAMS.fields_by_name['slash_fraction_downtime']._options = None
    _PARAMS.fields_by_name['slash_fraction_downtime']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xa8\xe7\xb0*\x01'
    _PARAMS._options = None
    _PARAMS._serialized_options = b'\x8a\xe7\xb0*\x1ccosmos-sdk/x/slashing/Params'
    _globals['_VALIDATORSIGNINGINFO']._serialized_start = 201
    _globals['_VALIDATORSIGNINGINFO']._serialized_end = 436
    _globals['_PARAMS']._serialized_start = 439
    _globals['_PARAMS']._serialized_end = 845