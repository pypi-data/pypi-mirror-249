"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....cosmos.base.query.v1beta1 import pagination_pb2 as cosmos_dot_base_dot_query_dot_v1beta1_dot_pagination__pb2
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from ....cosmos.bank.v1beta1 import bank_pb2 as cosmos_dot_bank_dot_v1beta1_dot_bank__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from ....cosmos.query.v1 import query_pb2 as cosmos_dot_query_dot_v1_dot_query__pb2
from ....amino import amino_pb2 as amino_dot_amino__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fcosmos/bank/v1beta1/query.proto\x12\x13cosmos.bank.v1beta1\x1a*cosmos/base/query/v1beta1/pagination.proto\x1a\x14gogoproto/gogo.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a\x1ecosmos/bank/v1beta1/bank.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x1bcosmos/query/v1/query.proto\x1a\x11amino/amino.proto"Y\n\x13QueryBalanceRequest\x12)\n\x07address\x18\x01 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString\x12\r\n\x05denom\x18\x02 \x01(\t:\x08\x88\xa0\x1f\x00\xe8\xa0\x1f\x00"B\n\x14QueryBalanceResponse\x12*\n\x07balance\x18\x01 \x01(\x0b2\x19.cosmos.base.v1beta1.Coin"\x8a\x01\n\x17QueryAllBalancesRequest\x12)\n\x07address\x18\x01 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest:\x08\x88\xa0\x1f\x00\xe8\xa0\x1f\x00"\xbb\x01\n\x18QueryAllBalancesResponse\x12b\n\x08balances\x18\x01 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB5\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xa8\xe7\xb0*\x01\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"\x90\x01\n\x1dQuerySpendableBalancesRequest\x12)\n\x07address\x18\x01 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest:\x08\x88\xa0\x1f\x00\xe8\xa0\x1f\x00"\xc1\x01\n\x1eQuerySpendableBalancesResponse\x12b\n\x08balances\x18\x01 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB5\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xa8\xe7\xb0*\x01\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"i\n#QuerySpendableBalanceByDenomRequest\x12)\n\x07address\x18\x01 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString\x12\r\n\x05denom\x18\x02 \x01(\t:\x08\x88\xa0\x1f\x00\xe8\xa0\x1f\x00"R\n$QuerySpendableBalanceByDenomResponse\x12*\n\x07balance\x18\x01 \x01(\x0b2\x19.cosmos.base.v1beta1.Coin"_\n\x17QueryTotalSupplyRequest\x12:\n\npagination\x18\x01 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest:\x08\x88\xa0\x1f\x00\xe8\xa0\x1f\x00"\xb9\x01\n\x18QueryTotalSupplyResponse\x12`\n\x06supply\x18\x01 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB5\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xa8\xe7\xb0*\x01\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"%\n\x14QuerySupplyOfRequest\x12\r\n\x05denom\x18\x01 \x01(\t"M\n\x15QuerySupplyOfResponse\x124\n\x06amount\x18\x01 \x01(\x0b2\x19.cosmos.base.v1beta1.CoinB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01"l\n$QueryTotalSupplyWithoutOffsetRequest\x12:\n\npagination\x18\x01 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest:\x08\x88\xa0\x1f\x00\xe8\xa0\x1f\x00"\xc1\x01\n%QueryTotalSupplyWithoutOffsetResponse\x12[\n\x06supply\x18\x01 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"2\n!QuerySupplyOfWithoutOffsetRequest\x12\r\n\x05denom\x18\x01 \x01(\t"U\n"QuerySupplyOfWithoutOffsetResponse\x12/\n\x06amount\x18\x01 \x01(\x0b2\x19.cosmos.base.v1beta1.CoinB\x04\xc8\xde\x1f\x00"\x14\n\x12QueryParamsRequest"M\n\x13QueryParamsResponse\x126\n\x06params\x18\x01 \x01(\x0b2\x1b.cosmos.bank.v1beta1.ParamsB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01"X\n\x1aQueryDenomsMetadataRequest\x12:\n\npagination\x18\x01 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"\x97\x01\n\x1bQueryDenomsMetadataResponse\x12;\n\tmetadatas\x18\x01 \x03(\x0b2\x1d.cosmos.bank.v1beta1.MetadataB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"*\n\x19QueryDenomMetadataRequest\x12\r\n\x05denom\x18\x01 \x01(\t"X\n\x1aQueryDenomMetadataResponse\x12:\n\x08metadata\x18\x01 \x01(\x0b2\x1d.cosmos.bank.v1beta1.MetadataB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01"d\n\x17QueryDenomOwnersRequest\x12\r\n\x05denom\x18\x01 \x01(\t\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"n\n\nDenomOwner\x12)\n\x07address\x18\x01 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString\x125\n\x07balance\x18\x02 \x01(\x0b2\x19.cosmos.base.v1beta1.CoinB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01"\x8e\x01\n\x18QueryDenomOwnersResponse\x125\n\x0cdenom_owners\x18\x01 \x03(\x0b2\x1f.cosmos.bank.v1beta1.DenomOwner\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"e\n\x17QuerySendEnabledRequest\x12\x0e\n\x06denoms\x18\x01 \x03(\t\x12:\n\npagination\x18c \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"\x8f\x01\n\x18QuerySendEnabledResponse\x126\n\x0csend_enabled\x18\x01 \x03(\x0b2 .cosmos.bank.v1beta1.SendEnabled\x12;\n\npagination\x18c \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse2\xc1\x11\n\x05Query\x12\x9d\x01\n\x07Balance\x12(.cosmos.bank.v1beta1.QueryBalanceRequest\x1a).cosmos.bank.v1beta1.QueryBalanceResponse"=\x88\xe7\xb0*\x01\x82\xd3\xe4\x93\x022\x120/cosmos/bank/v1beta1/balances/{address}/by_denom\x12\xa0\x01\n\x0bAllBalances\x12,.cosmos.bank.v1beta1.QueryAllBalancesRequest\x1a-.cosmos.bank.v1beta1.QueryAllBalancesResponse"4\x88\xe7\xb0*\x01\x82\xd3\xe4\x93\x02)\x12\'/cosmos/bank/v1beta1/balances/{address}\x12\xbc\x01\n\x11SpendableBalances\x122.cosmos.bank.v1beta1.QuerySpendableBalancesRequest\x1a3.cosmos.bank.v1beta1.QuerySpendableBalancesResponse">\x88\xe7\xb0*\x01\x82\xd3\xe4\x93\x023\x121/cosmos/bank/v1beta1/spendable_balances/{address}\x12\xd7\x01\n\x17SpendableBalanceByDenom\x128.cosmos.bank.v1beta1.QuerySpendableBalanceByDenomRequest\x1a9.cosmos.bank.v1beta1.QuerySpendableBalanceByDenomResponse"G\x88\xe7\xb0*\x01\x82\xd3\xe4\x93\x02<\x12:/cosmos/bank/v1beta1/spendable_balances/{address}/by_denom\x12\x94\x01\n\x0bTotalSupply\x12,.cosmos.bank.v1beta1.QueryTotalSupplyRequest\x1a-.cosmos.bank.v1beta1.QueryTotalSupplyResponse"(\x88\xe7\xb0*\x01\x82\xd3\xe4\x93\x02\x1d\x12\x1b/cosmos/bank/v1beta1/supply\x12\x94\x01\n\x08SupplyOf\x12).cosmos.bank.v1beta1.QuerySupplyOfRequest\x1a*.cosmos.bank.v1beta1.QuerySupplyOfResponse"1\x88\xe7\xb0*\x01\x82\xd3\xe4\x93\x02&\x12$/cosmos/bank/v1beta1/supply/by_denom\x12\xc5\x01\n\x18TotalSupplyWithoutOffset\x129.cosmos.bank.v1beta1.QueryTotalSupplyWithoutOffsetRequest\x1a:.cosmos.bank.v1beta1.QueryTotalSupplyWithoutOffsetResponse"2\x82\xd3\xe4\x93\x02,\x12*/cosmos/bank/v1beta1/supply_without_offset\x12\xc4\x01\n\x15SupplyOfWithoutOffset\x126.cosmos.bank.v1beta1.QuerySupplyOfWithoutOffsetRequest\x1a7.cosmos.bank.v1beta1.QuerySupplyOfWithoutOffsetResponse":\x82\xd3\xe4\x93\x024\x122/cosmos/bank/v1beta1/supply_without_offset/{denom}\x12\x85\x01\n\x06Params\x12\'.cosmos.bank.v1beta1.QueryParamsRequest\x1a(.cosmos.bank.v1beta1.QueryParamsResponse"(\x88\xe7\xb0*\x01\x82\xd3\xe4\x93\x02\x1d\x12\x1b/cosmos/bank/v1beta1/params\x12\xab\x01\n\rDenomMetadata\x12..cosmos.bank.v1beta1.QueryDenomMetadataRequest\x1a/.cosmos.bank.v1beta1.QueryDenomMetadataResponse"9\x88\xe7\xb0*\x01\x82\xd3\xe4\x93\x02.\x12,/cosmos/bank/v1beta1/denoms_metadata/{denom}\x12\xa6\x01\n\x0eDenomsMetadata\x12/.cosmos.bank.v1beta1.QueryDenomsMetadataRequest\x1a0.cosmos.bank.v1beta1.QueryDenomsMetadataResponse"1\x88\xe7\xb0*\x01\x82\xd3\xe4\x93\x02&\x12$/cosmos/bank/v1beta1/denoms_metadata\x12\xa2\x01\n\x0bDenomOwners\x12,.cosmos.bank.v1beta1.QueryDenomOwnersRequest\x1a-.cosmos.bank.v1beta1.QueryDenomOwnersResponse"6\x88\xe7\xb0*\x01\x82\xd3\xe4\x93\x02+\x12)/cosmos/bank/v1beta1/denom_owners/{denom}\x12\x9a\x01\n\x0bSendEnabled\x12,.cosmos.bank.v1beta1.QuerySendEnabledRequest\x1a-.cosmos.bank.v1beta1.QuerySendEnabledResponse".\x88\xe7\xb0*\x01\x82\xd3\xe4\x93\x02#\x12!/cosmos/bank/v1beta1/send_enabledB+Z)github.com/cosmos/cosmos-sdk/x/bank/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.bank.v1beta1.query_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z)github.com/cosmos/cosmos-sdk/x/bank/types'
    _QUERYBALANCEREQUEST.fields_by_name['address']._options = None
    _QUERYBALANCEREQUEST.fields_by_name['address']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _QUERYBALANCEREQUEST._options = None
    _QUERYBALANCEREQUEST._serialized_options = b'\x88\xa0\x1f\x00\xe8\xa0\x1f\x00'
    _QUERYALLBALANCESREQUEST.fields_by_name['address']._options = None
    _QUERYALLBALANCESREQUEST.fields_by_name['address']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _QUERYALLBALANCESREQUEST._options = None
    _QUERYALLBALANCESREQUEST._serialized_options = b'\x88\xa0\x1f\x00\xe8\xa0\x1f\x00'
    _QUERYALLBALANCESRESPONSE.fields_by_name['balances']._options = None
    _QUERYALLBALANCESRESPONSE.fields_by_name['balances']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xa8\xe7\xb0*\x01'
    _QUERYSPENDABLEBALANCESREQUEST.fields_by_name['address']._options = None
    _QUERYSPENDABLEBALANCESREQUEST.fields_by_name['address']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _QUERYSPENDABLEBALANCESREQUEST._options = None
    _QUERYSPENDABLEBALANCESREQUEST._serialized_options = b'\x88\xa0\x1f\x00\xe8\xa0\x1f\x00'
    _QUERYSPENDABLEBALANCESRESPONSE.fields_by_name['balances']._options = None
    _QUERYSPENDABLEBALANCESRESPONSE.fields_by_name['balances']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xa8\xe7\xb0*\x01'
    _QUERYSPENDABLEBALANCEBYDENOMREQUEST.fields_by_name['address']._options = None
    _QUERYSPENDABLEBALANCEBYDENOMREQUEST.fields_by_name['address']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _QUERYSPENDABLEBALANCEBYDENOMREQUEST._options = None
    _QUERYSPENDABLEBALANCEBYDENOMREQUEST._serialized_options = b'\x88\xa0\x1f\x00\xe8\xa0\x1f\x00'
    _QUERYTOTALSUPPLYREQUEST._options = None
    _QUERYTOTALSUPPLYREQUEST._serialized_options = b'\x88\xa0\x1f\x00\xe8\xa0\x1f\x00'
    _QUERYTOTALSUPPLYRESPONSE.fields_by_name['supply']._options = None
    _QUERYTOTALSUPPLYRESPONSE.fields_by_name['supply']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xa8\xe7\xb0*\x01'
    _QUERYSUPPLYOFRESPONSE.fields_by_name['amount']._options = None
    _QUERYSUPPLYOFRESPONSE.fields_by_name['amount']._serialized_options = b'\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01'
    _QUERYTOTALSUPPLYWITHOUTOFFSETREQUEST._options = None
    _QUERYTOTALSUPPLYWITHOUTOFFSETREQUEST._serialized_options = b'\x88\xa0\x1f\x00\xe8\xa0\x1f\x00'
    _QUERYTOTALSUPPLYWITHOUTOFFSETRESPONSE.fields_by_name['supply']._options = None
    _QUERYTOTALSUPPLYWITHOUTOFFSETRESPONSE.fields_by_name['supply']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _QUERYSUPPLYOFWITHOUTOFFSETRESPONSE.fields_by_name['amount']._options = None
    _QUERYSUPPLYOFWITHOUTOFFSETRESPONSE.fields_by_name['amount']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYPARAMSRESPONSE.fields_by_name['params']._options = None
    _QUERYPARAMSRESPONSE.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01'
    _QUERYDENOMSMETADATARESPONSE.fields_by_name['metadatas']._options = None
    _QUERYDENOMSMETADATARESPONSE.fields_by_name['metadatas']._serialized_options = b'\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01'
    _QUERYDENOMMETADATARESPONSE.fields_by_name['metadata']._options = None
    _QUERYDENOMMETADATARESPONSE.fields_by_name['metadata']._serialized_options = b'\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01'
    _DENOMOWNER.fields_by_name['address']._options = None
    _DENOMOWNER.fields_by_name['address']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _DENOMOWNER.fields_by_name['balance']._options = None
    _DENOMOWNER.fields_by_name['balance']._serialized_options = b'\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01'
    _QUERY.methods_by_name['Balance']._options = None
    _QUERY.methods_by_name['Balance']._serialized_options = b'\x88\xe7\xb0*\x01\x82\xd3\xe4\x93\x022\x120/cosmos/bank/v1beta1/balances/{address}/by_denom'
    _QUERY.methods_by_name['AllBalances']._options = None
    _QUERY.methods_by_name['AllBalances']._serialized_options = b"\x88\xe7\xb0*\x01\x82\xd3\xe4\x93\x02)\x12'/cosmos/bank/v1beta1/balances/{address}"
    _QUERY.methods_by_name['SpendableBalances']._options = None
    _QUERY.methods_by_name['SpendableBalances']._serialized_options = b'\x88\xe7\xb0*\x01\x82\xd3\xe4\x93\x023\x121/cosmos/bank/v1beta1/spendable_balances/{address}'
    _QUERY.methods_by_name['SpendableBalanceByDenom']._options = None
    _QUERY.methods_by_name['SpendableBalanceByDenom']._serialized_options = b'\x88\xe7\xb0*\x01\x82\xd3\xe4\x93\x02<\x12:/cosmos/bank/v1beta1/spendable_balances/{address}/by_denom'
    _QUERY.methods_by_name['TotalSupply']._options = None
    _QUERY.methods_by_name['TotalSupply']._serialized_options = b'\x88\xe7\xb0*\x01\x82\xd3\xe4\x93\x02\x1d\x12\x1b/cosmos/bank/v1beta1/supply'
    _QUERY.methods_by_name['SupplyOf']._options = None
    _QUERY.methods_by_name['SupplyOf']._serialized_options = b'\x88\xe7\xb0*\x01\x82\xd3\xe4\x93\x02&\x12$/cosmos/bank/v1beta1/supply/by_denom'
    _QUERY.methods_by_name['TotalSupplyWithoutOffset']._options = None
    _QUERY.methods_by_name['TotalSupplyWithoutOffset']._serialized_options = b'\x82\xd3\xe4\x93\x02,\x12*/cosmos/bank/v1beta1/supply_without_offset'
    _QUERY.methods_by_name['SupplyOfWithoutOffset']._options = None
    _QUERY.methods_by_name['SupplyOfWithoutOffset']._serialized_options = b'\x82\xd3\xe4\x93\x024\x122/cosmos/bank/v1beta1/supply_without_offset/{denom}'
    _QUERY.methods_by_name['Params']._options = None
    _QUERY.methods_by_name['Params']._serialized_options = b'\x88\xe7\xb0*\x01\x82\xd3\xe4\x93\x02\x1d\x12\x1b/cosmos/bank/v1beta1/params'
    _QUERY.methods_by_name['DenomMetadata']._options = None
    _QUERY.methods_by_name['DenomMetadata']._serialized_options = b'\x88\xe7\xb0*\x01\x82\xd3\xe4\x93\x02.\x12,/cosmos/bank/v1beta1/denoms_metadata/{denom}'
    _QUERY.methods_by_name['DenomsMetadata']._options = None
    _QUERY.methods_by_name['DenomsMetadata']._serialized_options = b'\x88\xe7\xb0*\x01\x82\xd3\xe4\x93\x02&\x12$/cosmos/bank/v1beta1/denoms_metadata'
    _QUERY.methods_by_name['DenomOwners']._options = None
    _QUERY.methods_by_name['DenomOwners']._serialized_options = b'\x88\xe7\xb0*\x01\x82\xd3\xe4\x93\x02+\x12)/cosmos/bank/v1beta1/denom_owners/{denom}'
    _QUERY.methods_by_name['SendEnabled']._options = None
    _QUERY.methods_by_name['SendEnabled']._serialized_options = b'\x88\xe7\xb0*\x01\x82\xd3\xe4\x93\x02#\x12!/cosmos/bank/v1beta1/send_enabled'
    _globals['_QUERYBALANCEREQUEST']._serialized_start = 291
    _globals['_QUERYBALANCEREQUEST']._serialized_end = 380
    _globals['_QUERYBALANCERESPONSE']._serialized_start = 382
    _globals['_QUERYBALANCERESPONSE']._serialized_end = 448
    _globals['_QUERYALLBALANCESREQUEST']._serialized_start = 451
    _globals['_QUERYALLBALANCESREQUEST']._serialized_end = 589
    _globals['_QUERYALLBALANCESRESPONSE']._serialized_start = 592
    _globals['_QUERYALLBALANCESRESPONSE']._serialized_end = 779
    _globals['_QUERYSPENDABLEBALANCESREQUEST']._serialized_start = 782
    _globals['_QUERYSPENDABLEBALANCESREQUEST']._serialized_end = 926
    _globals['_QUERYSPENDABLEBALANCESRESPONSE']._serialized_start = 929
    _globals['_QUERYSPENDABLEBALANCESRESPONSE']._serialized_end = 1122
    _globals['_QUERYSPENDABLEBALANCEBYDENOMREQUEST']._serialized_start = 1124
    _globals['_QUERYSPENDABLEBALANCEBYDENOMREQUEST']._serialized_end = 1229
    _globals['_QUERYSPENDABLEBALANCEBYDENOMRESPONSE']._serialized_start = 1231
    _globals['_QUERYSPENDABLEBALANCEBYDENOMRESPONSE']._serialized_end = 1313
    _globals['_QUERYTOTALSUPPLYREQUEST']._serialized_start = 1315
    _globals['_QUERYTOTALSUPPLYREQUEST']._serialized_end = 1410
    _globals['_QUERYTOTALSUPPLYRESPONSE']._serialized_start = 1413
    _globals['_QUERYTOTALSUPPLYRESPONSE']._serialized_end = 1598
    _globals['_QUERYSUPPLYOFREQUEST']._serialized_start = 1600
    _globals['_QUERYSUPPLYOFREQUEST']._serialized_end = 1637
    _globals['_QUERYSUPPLYOFRESPONSE']._serialized_start = 1639
    _globals['_QUERYSUPPLYOFRESPONSE']._serialized_end = 1716
    _globals['_QUERYTOTALSUPPLYWITHOUTOFFSETREQUEST']._serialized_start = 1718
    _globals['_QUERYTOTALSUPPLYWITHOUTOFFSETREQUEST']._serialized_end = 1826
    _globals['_QUERYTOTALSUPPLYWITHOUTOFFSETRESPONSE']._serialized_start = 1829
    _globals['_QUERYTOTALSUPPLYWITHOUTOFFSETRESPONSE']._serialized_end = 2022
    _globals['_QUERYSUPPLYOFWITHOUTOFFSETREQUEST']._serialized_start = 2024
    _globals['_QUERYSUPPLYOFWITHOUTOFFSETREQUEST']._serialized_end = 2074
    _globals['_QUERYSUPPLYOFWITHOUTOFFSETRESPONSE']._serialized_start = 2076
    _globals['_QUERYSUPPLYOFWITHOUTOFFSETRESPONSE']._serialized_end = 2161
    _globals['_QUERYPARAMSREQUEST']._serialized_start = 2163
    _globals['_QUERYPARAMSREQUEST']._serialized_end = 2183
    _globals['_QUERYPARAMSRESPONSE']._serialized_start = 2185
    _globals['_QUERYPARAMSRESPONSE']._serialized_end = 2262
    _globals['_QUERYDENOMSMETADATAREQUEST']._serialized_start = 2264
    _globals['_QUERYDENOMSMETADATAREQUEST']._serialized_end = 2352
    _globals['_QUERYDENOMSMETADATARESPONSE']._serialized_start = 2355
    _globals['_QUERYDENOMSMETADATARESPONSE']._serialized_end = 2506
    _globals['_QUERYDENOMMETADATAREQUEST']._serialized_start = 2508
    _globals['_QUERYDENOMMETADATAREQUEST']._serialized_end = 2550
    _globals['_QUERYDENOMMETADATARESPONSE']._serialized_start = 2552
    _globals['_QUERYDENOMMETADATARESPONSE']._serialized_end = 2640
    _globals['_QUERYDENOMOWNERSREQUEST']._serialized_start = 2642
    _globals['_QUERYDENOMOWNERSREQUEST']._serialized_end = 2742
    _globals['_DENOMOWNER']._serialized_start = 2744
    _globals['_DENOMOWNER']._serialized_end = 2854
    _globals['_QUERYDENOMOWNERSRESPONSE']._serialized_start = 2857
    _globals['_QUERYDENOMOWNERSRESPONSE']._serialized_end = 2999
    _globals['_QUERYSENDENABLEDREQUEST']._serialized_start = 3001
    _globals['_QUERYSENDENABLEDREQUEST']._serialized_end = 3102
    _globals['_QUERYSENDENABLEDRESPONSE']._serialized_start = 3105
    _globals['_QUERYSENDENABLEDRESPONSE']._serialized_end = 3248
    _globals['_QUERY']._serialized_start = 3251
    _globals['_QUERY']._serialized_end = 5492