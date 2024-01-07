"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from ....cosmos.msg.v1 import msg_pb2 as cosmos_dot_msg_dot_v1_dot_msg__pb2
from ....tendermint.types import params_pb2 as tendermint_dot_types_dot_params__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1ccosmos/consensus/v1/tx.proto\x12\x13cosmos.consensus.v1\x1a\x19cosmos_proto/cosmos.proto\x1a\x17cosmos/msg/v1/msg.proto\x1a\x1dtendermint/types/params.proto"\xe6\x01\n\x0fMsgUpdateParams\x12+\n\tauthority\x18\x01 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString\x12,\n\x05block\x18\x02 \x01(\x0b2\x1d.tendermint.types.BlockParams\x122\n\x08evidence\x18\x03 \x01(\x0b2 .tendermint.types.EvidenceParams\x124\n\tvalidator\x18\x04 \x01(\x0b2!.tendermint.types.ValidatorParams:\x0e\x82\xe7\xb0*\tauthority"\x19\n\x17MsgUpdateParamsResponse2i\n\x03Msg\x12b\n\x0cUpdateParams\x12$.cosmos.consensus.v1.MsgUpdateParams\x1a,.cosmos.consensus.v1.MsgUpdateParamsResponseB0Z.github.com/cosmos/cosmos-sdk/x/consensus/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.consensus.v1.tx_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z.github.com/cosmos/cosmos-sdk/x/consensus/types'
    _MSGUPDATEPARAMS.fields_by_name['authority']._options = None
    _MSGUPDATEPARAMS.fields_by_name['authority']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _MSGUPDATEPARAMS._options = None
    _MSGUPDATEPARAMS._serialized_options = b'\x82\xe7\xb0*\tauthority'
    _globals['_MSGUPDATEPARAMS']._serialized_start = 137
    _globals['_MSGUPDATEPARAMS']._serialized_end = 367
    _globals['_MSGUPDATEPARAMSRESPONSE']._serialized_start = 369
    _globals['_MSGUPDATEPARAMSRESPONSE']._serialized_end = 394
    _globals['_MSG']._serialized_start = 396
    _globals['_MSG']._serialized_end = 501