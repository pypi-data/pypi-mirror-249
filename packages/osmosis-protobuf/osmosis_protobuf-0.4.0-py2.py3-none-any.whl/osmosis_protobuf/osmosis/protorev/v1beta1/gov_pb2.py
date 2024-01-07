"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....amino import amino_pb2 as amino_dot_amino__pb2
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from ....osmosis.protorev.v1beta1 import protorev_pb2 as osmosis_dot_protorev_dot_v1beta1_dot_protorev__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n"osmosis/protorev/v1beta1/gov.proto\x12\x18osmosis.protorev.v1beta1\x1a\x11amino/amino.proto\x1a\x14gogoproto/gogo.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\'osmosis/protorev/v1beta1/protorev.proto"\xa4\x01\n\x1aSetProtoRevEnabledProposal\x12\r\n\x05title\x18\x01 \x01(\t\x12\x13\n\x0bdescription\x18\x02 \x01(\t\x12\x0f\n\x07enabled\x18\x03 \x01(\x08:Q\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xe8\xa0\x1f\x01\xca\xb4-\x1acosmos.gov.v1beta1.Content\x8a\xe7\xb0*"osmosis/SetProtoRevEnabledProposal"\xae\x01\n\x1fSetProtoRevAdminAccountProposal\x12\r\n\x05title\x18\x01 \x01(\t\x12\x13\n\x0bdescription\x18\x02 \x01(\t\x12\x0f\n\x07account\x18\x03 \x01(\t:V\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xe8\xa0\x1f\x01\xca\xb4-\x1acosmos.gov.v1beta1.Content\x8a\xe7\xb0*\'osmosis/SetProtoRevAdminAccountProposalB6Z4github.com/osmosis-labs/osmosis/v21/x/protorev/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.protorev.v1beta1.gov_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z4github.com/osmosis-labs/osmosis/v21/x/protorev/types'
    _SETPROTOREVENABLEDPROPOSAL._options = None
    _SETPROTOREVENABLEDPROPOSAL._serialized_options = b'\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xe8\xa0\x1f\x01\xca\xb4-\x1acosmos.gov.v1beta1.Content\x8a\xe7\xb0*"osmosis/SetProtoRevEnabledProposal'
    _SETPROTOREVADMINACCOUNTPROPOSAL._options = None
    _SETPROTOREVADMINACCOUNTPROPOSAL._serialized_options = b"\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xe8\xa0\x1f\x01\xca\xb4-\x1acosmos.gov.v1beta1.Content\x8a\xe7\xb0*'osmosis/SetProtoRevAdminAccountProposal"
    _globals['_SETPROTOREVENABLEDPROPOSAL']._serialized_start = 174
    _globals['_SETPROTOREVENABLEDPROPOSAL']._serialized_end = 338
    _globals['_SETPROTOREVADMINACCOUNTPROPOSAL']._serialized_start = 341
    _globals['_SETPROTOREVADMINACCOUNTPROPOSAL']._serialized_end = 515