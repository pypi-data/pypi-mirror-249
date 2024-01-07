"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from ....amino import amino_pb2 as amino_dot_amino__pb2
from ....osmosis.txfees.v1beta1 import feetoken_pb2 as osmosis_dot_txfees_dot_v1beta1_dot_feetoken__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n osmosis/txfees/v1beta1/gov.proto\x12\x16osmosis.txfees.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x11amino/amino.proto\x1a%osmosis/txfees/v1beta1/feetoken.proto"\x85\x02\n\x16UpdateFeeTokenProposal\x12\x1f\n\x05title\x18\x01 \x01(\tB\x10\xf2\xde\x1f\x0cyaml:"title"\x12+\n\x0bdescription\x18\x02 \x01(\tB\x16\xf2\xde\x1f\x12yaml:"description"\x12N\n\tfeetokens\x18\x03 \x03(\x0b2 .osmosis.txfees.v1beta1.FeeTokenB\x19\xc8\xde\x1f\x00\xf2\xde\x1f\x11yaml:"fee_tokens":M\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xe8\xa0\x1f\x01\xca\xb4-\x1acosmos.gov.v1beta1.Content\x8a\xe7\xb0*\x1eosmosis/UpdateFeeTokenProposalB4Z2github.com/osmosis-labs/osmosis/v21/x/txfees/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.txfees.v1beta1.gov_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z2github.com/osmosis-labs/osmosis/v21/x/txfees/types'
    _UPDATEFEETOKENPROPOSAL.fields_by_name['title']._options = None
    _UPDATEFEETOKENPROPOSAL.fields_by_name['title']._serialized_options = b'\xf2\xde\x1f\x0cyaml:"title"'
    _UPDATEFEETOKENPROPOSAL.fields_by_name['description']._options = None
    _UPDATEFEETOKENPROPOSAL.fields_by_name['description']._serialized_options = b'\xf2\xde\x1f\x12yaml:"description"'
    _UPDATEFEETOKENPROPOSAL.fields_by_name['feetokens']._options = None
    _UPDATEFEETOKENPROPOSAL.fields_by_name['feetokens']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x11yaml:"fee_tokens"'
    _UPDATEFEETOKENPROPOSAL._options = None
    _UPDATEFEETOKENPROPOSAL._serialized_options = b'\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xe8\xa0\x1f\x01\xca\xb4-\x1acosmos.gov.v1beta1.Content\x8a\xe7\xb0*\x1eosmosis/UpdateFeeTokenProposal'
    _globals['_UPDATEFEETOKENPROPOSAL']._serialized_start = 168
    _globals['_UPDATEFEETOKENPROPOSAL']._serialized_end = 429