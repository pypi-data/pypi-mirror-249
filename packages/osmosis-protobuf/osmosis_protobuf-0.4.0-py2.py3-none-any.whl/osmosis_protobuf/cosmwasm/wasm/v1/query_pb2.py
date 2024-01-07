"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....cosmwasm.wasm.v1 import types_pb2 as cosmwasm_dot_wasm_dot_v1_dot_types__pb2
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from ....cosmos.base.query.v1beta1 import pagination_pb2 as cosmos_dot_base_dot_query_dot_v1beta1_dot_pagination__pb2
from ....amino import amino_pb2 as amino_dot_amino__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1ccosmwasm/wasm/v1/query.proto\x12\x10cosmwasm.wasm.v1\x1a\x14gogoproto/gogo.proto\x1a\x1ccosmwasm/wasm/v1/types.proto\x1a\x1cgoogle/api/annotations.proto\x1a*cosmos/base/query/v1beta1/pagination.proto\x1a\x11amino/amino.proto"+\n\x18QueryContractInfoRequest\x12\x0f\n\x07address\x18\x01 \x01(\t"|\n\x19QueryContractInfoResponse\x12\x0f\n\x07address\x18\x01 \x01(\t\x12H\n\rcontract_info\x18\x02 \x01(\x0b2\x1e.cosmwasm.wasm.v1.ContractInfoB\x11\xc8\xde\x1f\x00\xd0\xde\x1f\x01\xea\xde\x1f\x00\xa8\xe7\xb0*\x01:\x04\xe8\xa0\x1f\x01"j\n\x1bQueryContractHistoryRequest\x12\x0f\n\x07address\x18\x01 \x01(\t\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"\xa3\x01\n\x1cQueryContractHistoryResponse\x12F\n\x07entries\x18\x01 \x03(\x0b2*.cosmwasm.wasm.v1.ContractCodeHistoryEntryB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"j\n\x1bQueryContractsByCodeRequest\x12\x0f\n\x07code_id\x18\x01 \x01(\x04\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"n\n\x1cQueryContractsByCodeResponse\x12\x11\n\tcontracts\x18\x01 \x03(\t\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"k\n\x1cQueryAllContractStateRequest\x12\x0f\n\x07address\x18\x01 \x01(\t\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"\x90\x01\n\x1dQueryAllContractStateResponse\x122\n\x06models\x18\x01 \x03(\x0b2\x17.cosmwasm.wasm.v1.ModelB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"C\n\x1cQueryRawContractStateRequest\x12\x0f\n\x07address\x18\x01 \x01(\t\x12\x12\n\nquery_data\x18\x02 \x01(\x0c"-\n\x1dQueryRawContractStateResponse\x12\x0c\n\x04data\x18\x01 \x01(\x0c"]\n\x1eQuerySmartContractStateRequest\x12\x0f\n\x07address\x18\x01 \x01(\t\x12*\n\nquery_data\x18\x02 \x01(\x0cB\x16\xfa\xde\x1f\x12RawContractMessage"G\n\x1fQuerySmartContractStateResponse\x12$\n\x04data\x18\x01 \x01(\x0cB\x16\xfa\xde\x1f\x12RawContractMessage"#\n\x10QueryCodeRequest\x12\x0f\n\x07code_id\x18\x01 \x01(\x04"\xec\x01\n\x10CodeInfoResponse\x12!\n\x07code_id\x18\x01 \x01(\x04B\x10\xe2\xde\x1f\x06CodeID\xea\xde\x1f\x02id\x12\x0f\n\x07creator\x18\x02 \x01(\t\x12G\n\tdata_hash\x18\x03 \x01(\x0cB4\xfa\xde\x1f0github.com/cometbft/cometbft/libs/bytes.HexBytes\x12I\n\x16instantiate_permission\x18\x06 \x01(\x0b2\x1e.cosmwasm.wasm.v1.AccessConfigB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01:\x04\xe8\xa0\x1f\x01J\x04\x08\x04\x10\x05J\x04\x08\x05\x10\x06"r\n\x11QueryCodeResponse\x12?\n\tcode_info\x18\x01 \x01(\x0b2".cosmwasm.wasm.v1.CodeInfoResponseB\x08\xd0\xde\x1f\x01\xea\xde\x1f\x00\x12\x16\n\x04data\x18\x02 \x01(\x0cB\x08\xea\xde\x1f\x04data:\x04\xe8\xa0\x1f\x01"O\n\x11QueryCodesRequest\x12:\n\npagination\x18\x01 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"\x94\x01\n\x12QueryCodesResponse\x12A\n\ncode_infos\x18\x01 \x03(\x0b2".cosmwasm.wasm.v1.CodeInfoResponseB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"U\n\x17QueryPinnedCodesRequest\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"v\n\x18QueryPinnedCodesResponse\x12\x1d\n\x08code_ids\x18\x01 \x03(\x04B\x0b\xe2\xde\x1f\x07CodeIDs\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"\x14\n\x12QueryParamsRequest"J\n\x13QueryParamsResponse\x123\n\x06params\x18\x01 \x01(\x0b2\x18.cosmwasm.wasm.v1.ParamsB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01"u\n\x1eQueryContractsByCreatorRequest\x12\x17\n\x0fcreator_address\x18\x01 \x01(\t\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"z\n\x1fQueryContractsByCreatorResponse\x12\x1a\n\x12contract_addresses\x18\x01 \x03(\t\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse2\xc3\r\n\x05Query\x12\x95\x01\n\x0cContractInfo\x12*.cosmwasm.wasm.v1.QueryContractInfoRequest\x1a+.cosmwasm.wasm.v1.QueryContractInfoResponse",\x82\xd3\xe4\x93\x02&\x12$/cosmwasm/wasm/v1/contract/{address}\x12\xa6\x01\n\x0fContractHistory\x12-.cosmwasm.wasm.v1.QueryContractHistoryRequest\x1a..cosmwasm.wasm.v1.QueryContractHistoryResponse"4\x82\xd3\xe4\x93\x02.\x12,/cosmwasm/wasm/v1/contract/{address}/history\x12\xa4\x01\n\x0fContractsByCode\x12-.cosmwasm.wasm.v1.QueryContractsByCodeRequest\x1a..cosmwasm.wasm.v1.QueryContractsByCodeResponse"2\x82\xd3\xe4\x93\x02,\x12*/cosmwasm/wasm/v1/code/{code_id}/contracts\x12\xa7\x01\n\x10AllContractState\x12..cosmwasm.wasm.v1.QueryAllContractStateRequest\x1a/.cosmwasm.wasm.v1.QueryAllContractStateResponse"2\x82\xd3\xe4\x93\x02,\x12*/cosmwasm/wasm/v1/contract/{address}/state\x12\xb2\x01\n\x10RawContractState\x12..cosmwasm.wasm.v1.QueryRawContractStateRequest\x1a/.cosmwasm.wasm.v1.QueryRawContractStateResponse"=\x82\xd3\xe4\x93\x027\x125/cosmwasm/wasm/v1/contract/{address}/raw/{query_data}\x12\xba\x01\n\x12SmartContractState\x120.cosmwasm.wasm.v1.QuerySmartContractStateRequest\x1a1.cosmwasm.wasm.v1.QuerySmartContractStateResponse"?\x82\xd3\xe4\x93\x029\x127/cosmwasm/wasm/v1/contract/{address}/smart/{query_data}\x12y\n\x04Code\x12".cosmwasm.wasm.v1.QueryCodeRequest\x1a#.cosmwasm.wasm.v1.QueryCodeResponse"(\x82\xd3\xe4\x93\x02"\x12 /cosmwasm/wasm/v1/code/{code_id}\x12r\n\x05Codes\x12#.cosmwasm.wasm.v1.QueryCodesRequest\x1a$.cosmwasm.wasm.v1.QueryCodesResponse"\x1e\x82\xd3\xe4\x93\x02\x18\x12\x16/cosmwasm/wasm/v1/code\x12\x8c\x01\n\x0bPinnedCodes\x12).cosmwasm.wasm.v1.QueryPinnedCodesRequest\x1a*.cosmwasm.wasm.v1.QueryPinnedCodesResponse"&\x82\xd3\xe4\x93\x02 \x12\x1e/cosmwasm/wasm/v1/codes/pinned\x12}\n\x06Params\x12$.cosmwasm.wasm.v1.QueryParamsRequest\x1a%.cosmwasm.wasm.v1.QueryParamsResponse"&\x82\xd3\xe4\x93\x02 \x12\x1e/cosmwasm/wasm/v1/codes/params\x12\xb8\x01\n\x12ContractsByCreator\x120.cosmwasm.wasm.v1.QueryContractsByCreatorRequest\x1a1.cosmwasm.wasm.v1.QueryContractsByCreatorResponse"=\x82\xd3\xe4\x93\x027\x125/cosmwasm/wasm/v1/contracts/creator/{creator_address}B0Z&github.com/CosmWasm/wasmd/x/wasm/types\xc8\xe1\x1e\x00\xa8\xe2\x1e\x00b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmwasm.wasm.v1.query_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z&github.com/CosmWasm/wasmd/x/wasm/types\xc8\xe1\x1e\x00\xa8\xe2\x1e\x00'
    _QUERYCONTRACTINFORESPONSE.fields_by_name['contract_info']._options = None
    _QUERYCONTRACTINFORESPONSE.fields_by_name['contract_info']._serialized_options = b'\xc8\xde\x1f\x00\xd0\xde\x1f\x01\xea\xde\x1f\x00\xa8\xe7\xb0*\x01'
    _QUERYCONTRACTINFORESPONSE._options = None
    _QUERYCONTRACTINFORESPONSE._serialized_options = b'\xe8\xa0\x1f\x01'
    _QUERYCONTRACTHISTORYRESPONSE.fields_by_name['entries']._options = None
    _QUERYCONTRACTHISTORYRESPONSE.fields_by_name['entries']._serialized_options = b'\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01'
    _QUERYALLCONTRACTSTATERESPONSE.fields_by_name['models']._options = None
    _QUERYALLCONTRACTSTATERESPONSE.fields_by_name['models']._serialized_options = b'\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01'
    _QUERYSMARTCONTRACTSTATEREQUEST.fields_by_name['query_data']._options = None
    _QUERYSMARTCONTRACTSTATEREQUEST.fields_by_name['query_data']._serialized_options = b'\xfa\xde\x1f\x12RawContractMessage'
    _QUERYSMARTCONTRACTSTATERESPONSE.fields_by_name['data']._options = None
    _QUERYSMARTCONTRACTSTATERESPONSE.fields_by_name['data']._serialized_options = b'\xfa\xde\x1f\x12RawContractMessage'
    _CODEINFORESPONSE.fields_by_name['code_id']._options = None
    _CODEINFORESPONSE.fields_by_name['code_id']._serialized_options = b'\xe2\xde\x1f\x06CodeID\xea\xde\x1f\x02id'
    _CODEINFORESPONSE.fields_by_name['data_hash']._options = None
    _CODEINFORESPONSE.fields_by_name['data_hash']._serialized_options = b'\xfa\xde\x1f0github.com/cometbft/cometbft/libs/bytes.HexBytes'
    _CODEINFORESPONSE.fields_by_name['instantiate_permission']._options = None
    _CODEINFORESPONSE.fields_by_name['instantiate_permission']._serialized_options = b'\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01'
    _CODEINFORESPONSE._options = None
    _CODEINFORESPONSE._serialized_options = b'\xe8\xa0\x1f\x01'
    _QUERYCODERESPONSE.fields_by_name['code_info']._options = None
    _QUERYCODERESPONSE.fields_by_name['code_info']._serialized_options = b'\xd0\xde\x1f\x01\xea\xde\x1f\x00'
    _QUERYCODERESPONSE.fields_by_name['data']._options = None
    _QUERYCODERESPONSE.fields_by_name['data']._serialized_options = b'\xea\xde\x1f\x04data'
    _QUERYCODERESPONSE._options = None
    _QUERYCODERESPONSE._serialized_options = b'\xe8\xa0\x1f\x01'
    _QUERYCODESRESPONSE.fields_by_name['code_infos']._options = None
    _QUERYCODESRESPONSE.fields_by_name['code_infos']._serialized_options = b'\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01'
    _QUERYPINNEDCODESRESPONSE.fields_by_name['code_ids']._options = None
    _QUERYPINNEDCODESRESPONSE.fields_by_name['code_ids']._serialized_options = b'\xe2\xde\x1f\x07CodeIDs'
    _QUERYPARAMSRESPONSE.fields_by_name['params']._options = None
    _QUERYPARAMSRESPONSE.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01'
    _QUERY.methods_by_name['ContractInfo']._options = None
    _QUERY.methods_by_name['ContractInfo']._serialized_options = b'\x82\xd3\xe4\x93\x02&\x12$/cosmwasm/wasm/v1/contract/{address}'
    _QUERY.methods_by_name['ContractHistory']._options = None
    _QUERY.methods_by_name['ContractHistory']._serialized_options = b'\x82\xd3\xe4\x93\x02.\x12,/cosmwasm/wasm/v1/contract/{address}/history'
    _QUERY.methods_by_name['ContractsByCode']._options = None
    _QUERY.methods_by_name['ContractsByCode']._serialized_options = b'\x82\xd3\xe4\x93\x02,\x12*/cosmwasm/wasm/v1/code/{code_id}/contracts'
    _QUERY.methods_by_name['AllContractState']._options = None
    _QUERY.methods_by_name['AllContractState']._serialized_options = b'\x82\xd3\xe4\x93\x02,\x12*/cosmwasm/wasm/v1/contract/{address}/state'
    _QUERY.methods_by_name['RawContractState']._options = None
    _QUERY.methods_by_name['RawContractState']._serialized_options = b'\x82\xd3\xe4\x93\x027\x125/cosmwasm/wasm/v1/contract/{address}/raw/{query_data}'
    _QUERY.methods_by_name['SmartContractState']._options = None
    _QUERY.methods_by_name['SmartContractState']._serialized_options = b'\x82\xd3\xe4\x93\x029\x127/cosmwasm/wasm/v1/contract/{address}/smart/{query_data}'
    _QUERY.methods_by_name['Code']._options = None
    _QUERY.methods_by_name['Code']._serialized_options = b'\x82\xd3\xe4\x93\x02"\x12 /cosmwasm/wasm/v1/code/{code_id}'
    _QUERY.methods_by_name['Codes']._options = None
    _QUERY.methods_by_name['Codes']._serialized_options = b'\x82\xd3\xe4\x93\x02\x18\x12\x16/cosmwasm/wasm/v1/code'
    _QUERY.methods_by_name['PinnedCodes']._options = None
    _QUERY.methods_by_name['PinnedCodes']._serialized_options = b'\x82\xd3\xe4\x93\x02 \x12\x1e/cosmwasm/wasm/v1/codes/pinned'
    _QUERY.methods_by_name['Params']._options = None
    _QUERY.methods_by_name['Params']._serialized_options = b'\x82\xd3\xe4\x93\x02 \x12\x1e/cosmwasm/wasm/v1/codes/params'
    _QUERY.methods_by_name['ContractsByCreator']._options = None
    _QUERY.methods_by_name['ContractsByCreator']._serialized_options = b'\x82\xd3\xe4\x93\x027\x125/cosmwasm/wasm/v1/contracts/creator/{creator_address}'
    _globals['_QUERYCONTRACTINFOREQUEST']._serialized_start = 195
    _globals['_QUERYCONTRACTINFOREQUEST']._serialized_end = 238
    _globals['_QUERYCONTRACTINFORESPONSE']._serialized_start = 240
    _globals['_QUERYCONTRACTINFORESPONSE']._serialized_end = 364
    _globals['_QUERYCONTRACTHISTORYREQUEST']._serialized_start = 366
    _globals['_QUERYCONTRACTHISTORYREQUEST']._serialized_end = 472
    _globals['_QUERYCONTRACTHISTORYRESPONSE']._serialized_start = 475
    _globals['_QUERYCONTRACTHISTORYRESPONSE']._serialized_end = 638
    _globals['_QUERYCONTRACTSBYCODEREQUEST']._serialized_start = 640
    _globals['_QUERYCONTRACTSBYCODEREQUEST']._serialized_end = 746
    _globals['_QUERYCONTRACTSBYCODERESPONSE']._serialized_start = 748
    _globals['_QUERYCONTRACTSBYCODERESPONSE']._serialized_end = 858
    _globals['_QUERYALLCONTRACTSTATEREQUEST']._serialized_start = 860
    _globals['_QUERYALLCONTRACTSTATEREQUEST']._serialized_end = 967
    _globals['_QUERYALLCONTRACTSTATERESPONSE']._serialized_start = 970
    _globals['_QUERYALLCONTRACTSTATERESPONSE']._serialized_end = 1114
    _globals['_QUERYRAWCONTRACTSTATEREQUEST']._serialized_start = 1116
    _globals['_QUERYRAWCONTRACTSTATEREQUEST']._serialized_end = 1183
    _globals['_QUERYRAWCONTRACTSTATERESPONSE']._serialized_start = 1185
    _globals['_QUERYRAWCONTRACTSTATERESPONSE']._serialized_end = 1230
    _globals['_QUERYSMARTCONTRACTSTATEREQUEST']._serialized_start = 1232
    _globals['_QUERYSMARTCONTRACTSTATEREQUEST']._serialized_end = 1325
    _globals['_QUERYSMARTCONTRACTSTATERESPONSE']._serialized_start = 1327
    _globals['_QUERYSMARTCONTRACTSTATERESPONSE']._serialized_end = 1398
    _globals['_QUERYCODEREQUEST']._serialized_start = 1400
    _globals['_QUERYCODEREQUEST']._serialized_end = 1435
    _globals['_CODEINFORESPONSE']._serialized_start = 1438
    _globals['_CODEINFORESPONSE']._serialized_end = 1674
    _globals['_QUERYCODERESPONSE']._serialized_start = 1676
    _globals['_QUERYCODERESPONSE']._serialized_end = 1790
    _globals['_QUERYCODESREQUEST']._serialized_start = 1792
    _globals['_QUERYCODESREQUEST']._serialized_end = 1871
    _globals['_QUERYCODESRESPONSE']._serialized_start = 1874
    _globals['_QUERYCODESRESPONSE']._serialized_end = 2022
    _globals['_QUERYPINNEDCODESREQUEST']._serialized_start = 2024
    _globals['_QUERYPINNEDCODESREQUEST']._serialized_end = 2109
    _globals['_QUERYPINNEDCODESRESPONSE']._serialized_start = 2111
    _globals['_QUERYPINNEDCODESRESPONSE']._serialized_end = 2229
    _globals['_QUERYPARAMSREQUEST']._serialized_start = 2231
    _globals['_QUERYPARAMSREQUEST']._serialized_end = 2251
    _globals['_QUERYPARAMSRESPONSE']._serialized_start = 2253
    _globals['_QUERYPARAMSRESPONSE']._serialized_end = 2327
    _globals['_QUERYCONTRACTSBYCREATORREQUEST']._serialized_start = 2329
    _globals['_QUERYCONTRACTSBYCREATORREQUEST']._serialized_end = 2446
    _globals['_QUERYCONTRACTSBYCREATORRESPONSE']._serialized_start = 2448
    _globals['_QUERYCONTRACTSBYCREATORRESPONSE']._serialized_end = 2570
    _globals['_QUERY']._serialized_start = 2573
    _globals['_QUERY']._serialized_end = 4304