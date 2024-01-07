"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....osmosis.cosmwasmpool.v1beta1 import params_pb2 as osmosis_dot_cosmwasmpool_dot_v1beta1_dot_params__pb2
from ....osmosis.cosmwasmpool.v1beta1 import tx_pb2 as osmosis_dot_cosmwasmpool_dot_v1beta1_dot_tx__pb2
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from ....cosmos.base.query.v1beta1 import pagination_pb2 as cosmos_dot_base_dot_query_dot_v1beta1_dot_pagination__pb2
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n(osmosis/cosmwasmpool/v1beta1/query.proto\x12\x1cosmosis.cosmwasmpool.v1beta1\x1a\x14gogoproto/gogo.proto\x1a)osmosis/cosmwasmpool/v1beta1/params.proto\x1a%osmosis/cosmwasmpool/v1beta1/tx.proto\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a*cosmos/base/query/v1beta1/pagination.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x19google/protobuf/any.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x1fgoogle/protobuf/timestamp.proto"\x0f\n\rParamsRequest"L\n\x0eParamsResponse\x12:\n\x06params\x18\x01 \x01(\x0b2$.osmosis.cosmwasmpool.v1beta1.ParamsB\x04\xc8\xde\x1f\x00"J\n\x0cPoolsRequest\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"|\n\rPoolsResponse\x12.\n\x05pools\x18\x01 \x03(\x0b2\x14.google.protobuf.AnyB\t\xca\xb4-\x05PoolI\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"B\n\x1bContractInfoByPoolIdRequest\x12#\n\x07pool_id\x18\x01 \x01(\x04B\x12\xf2\xde\x1f\x0eyaml:"pool_id""z\n\x1cContractInfoByPoolIdResponse\x125\n\x10contract_address\x18\x01 \x01(\tB\x1b\xf2\xde\x1f\x17yaml:"contract_address"\x12#\n\x07code_id\x18\x02 \x01(\x04B\x12\xf2\xde\x1f\x0eyaml:"code_id"2\xf0\x03\n\x05Query\x12\x8d\x01\n\x05Pools\x12*.osmosis.cosmwasmpool.v1beta1.PoolsRequest\x1a+.osmosis.cosmwasmpool.v1beta1.PoolsResponse"+\x82\xd3\xe4\x93\x02%\x12#/osmosis/cosmwasmpool/v1beta1/pools\x12\x91\x01\n\x06Params\x12+.osmosis.cosmwasmpool.v1beta1.ParamsRequest\x1a,.osmosis.cosmwasmpool.v1beta1.ParamsResponse",\x82\xd3\xe4\x93\x02&\x12$/osmosis/cosmwasmpool/v1beta1/params\x12\xc2\x01\n\x14ContractInfoByPoolId\x129.osmosis.cosmwasmpool.v1beta1.ContractInfoByPoolIdRequest\x1a:.osmosis.cosmwasmpool.v1beta1.ContractInfoByPoolIdResponse"3\x82\xd3\xe4\x93\x02-\x12+/osmosis/cosmwasmpool/v1beta1/contract_infoBFZDgithub.com/osmosis-labs/osmosis/v21/x/cosmwasmpool/client/queryprotob\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.cosmwasmpool.v1beta1.query_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'ZDgithub.com/osmosis-labs/osmosis/v21/x/cosmwasmpool/client/queryproto'
    _PARAMSRESPONSE.fields_by_name['params']._options = None
    _PARAMSRESPONSE.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _POOLSRESPONSE.fields_by_name['pools']._options = None
    _POOLSRESPONSE.fields_by_name['pools']._serialized_options = b'\xca\xb4-\x05PoolI'
    _CONTRACTINFOBYPOOLIDREQUEST.fields_by_name['pool_id']._options = None
    _CONTRACTINFOBYPOOLIDREQUEST.fields_by_name['pool_id']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"pool_id"'
    _CONTRACTINFOBYPOOLIDRESPONSE.fields_by_name['contract_address']._options = None
    _CONTRACTINFOBYPOOLIDRESPONSE.fields_by_name['contract_address']._serialized_options = b'\xf2\xde\x1f\x17yaml:"contract_address"'
    _CONTRACTINFOBYPOOLIDRESPONSE.fields_by_name['code_id']._options = None
    _CONTRACTINFOBYPOOLIDRESPONSE.fields_by_name['code_id']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"code_id"'
    _QUERY.methods_by_name['Pools']._options = None
    _QUERY.methods_by_name['Pools']._serialized_options = b'\x82\xd3\xe4\x93\x02%\x12#/osmosis/cosmwasmpool/v1beta1/pools'
    _QUERY.methods_by_name['Params']._options = None
    _QUERY.methods_by_name['Params']._serialized_options = b'\x82\xd3\xe4\x93\x02&\x12$/osmosis/cosmwasmpool/v1beta1/params'
    _QUERY.methods_by_name['ContractInfoByPoolId']._options = None
    _QUERY.methods_by_name['ContractInfoByPoolId']._serialized_options = b'\x82\xd3\xe4\x93\x02-\x12+/osmosis/cosmwasmpool/v1beta1/contract_info'
    _globals['_PARAMSREQUEST']._serialized_start = 371
    _globals['_PARAMSREQUEST']._serialized_end = 386
    _globals['_PARAMSRESPONSE']._serialized_start = 388
    _globals['_PARAMSRESPONSE']._serialized_end = 464
    _globals['_POOLSREQUEST']._serialized_start = 466
    _globals['_POOLSREQUEST']._serialized_end = 540
    _globals['_POOLSRESPONSE']._serialized_start = 542
    _globals['_POOLSRESPONSE']._serialized_end = 666
    _globals['_CONTRACTINFOBYPOOLIDREQUEST']._serialized_start = 668
    _globals['_CONTRACTINFOBYPOOLIDREQUEST']._serialized_end = 734
    _globals['_CONTRACTINFOBYPOOLIDRESPONSE']._serialized_start = 736
    _globals['_CONTRACTINFOBYPOOLIDRESPONSE']._serialized_end = 858
    _globals['_QUERY']._serialized_start = 861
    _globals['_QUERY']._serialized_end = 1357