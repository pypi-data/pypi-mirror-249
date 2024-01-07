"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&osmosis/cosmwasmpool/v1beta1/gov.proto\x12\x1cosmosis.cosmwasmpool.v1beta1\x1a\x14gogoproto/gogo.proto"\x88\x01\n*UploadCosmWasmPoolCodeAndWhiteListProposal\x12\r\n\x05title\x18\x01 \x01(\t\x12\x13\n\x0bdescription\x18\x02 \x01(\t\x12(\n\x0ewasm_byte_code\x18\x03 \x01(\x0cB\x10\xe2\xde\x1f\x0cWASMByteCode:\x0c\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xe8\xa0\x1f\x01"\xb6\x01\n\x1cMigratePoolContractsProposal\x12\r\n\x05title\x18\x01 \x01(\t\x12\x13\n\x0bdescription\x18\x02 \x01(\t\x12\x10\n\x08pool_ids\x18\x03 \x03(\x04\x12\x13\n\x0bnew_code_id\x18\x04 \x01(\x04\x12(\n\x0ewasm_byte_code\x18\x05 \x01(\x0cB\x10\xe2\xde\x1f\x0cWASMByteCode\x12\x13\n\x0bmigrate_msg\x18\x06 \x01(\x0c:\x0c\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xe8\xa0\x1f\x01B:Z8github.com/osmosis-labs/osmosis/v21/x/cosmwasmpool/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.cosmwasmpool.v1beta1.gov_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z8github.com/osmosis-labs/osmosis/v21/x/cosmwasmpool/types'
    _UPLOADCOSMWASMPOOLCODEANDWHITELISTPROPOSAL.fields_by_name['wasm_byte_code']._options = None
    _UPLOADCOSMWASMPOOLCODEANDWHITELISTPROPOSAL.fields_by_name['wasm_byte_code']._serialized_options = b'\xe2\xde\x1f\x0cWASMByteCode'
    _UPLOADCOSMWASMPOOLCODEANDWHITELISTPROPOSAL._options = None
    _UPLOADCOSMWASMPOOLCODEANDWHITELISTPROPOSAL._serialized_options = b'\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xe8\xa0\x1f\x01'
    _MIGRATEPOOLCONTRACTSPROPOSAL.fields_by_name['wasm_byte_code']._options = None
    _MIGRATEPOOLCONTRACTSPROPOSAL.fields_by_name['wasm_byte_code']._serialized_options = b'\xe2\xde\x1f\x0cWASMByteCode'
    _MIGRATEPOOLCONTRACTSPROPOSAL._options = None
    _MIGRATEPOOLCONTRACTSPROPOSAL._serialized_options = b'\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xe8\xa0\x1f\x01'
    _globals['_UPLOADCOSMWASMPOOLCODEANDWHITELISTPROPOSAL']._serialized_start = 95
    _globals['_UPLOADCOSMWASMPOOLCODEANDWHITELISTPROPOSAL']._serialized_end = 231
    _globals['_MIGRATEPOOLCONTRACTSPROPOSAL']._serialized_start = 234
    _globals['_MIGRATEPOOLCONTRACTSPROPOSAL']._serialized_end = 416