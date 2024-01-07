"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....amino import amino_pb2 as amino_dot_amino__pb2
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from ....cosmos.bank.v1beta1 import bank_pb2 as cosmos_dot_bank_dot_v1beta1_dot_bank__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%osmosis/tokenfactory/v1beta1/tx.proto\x12\x1cosmosis.tokenfactory.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x11amino/amino.proto\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a\x1ecosmos/bank/v1beta1/bank.proto"\x82\x01\n\x0eMsgCreateDenom\x12!\n\x06sender\x18\x01 \x01(\tB\x11\xf2\xde\x1f\ryaml:"sender"\x12%\n\x08subdenom\x18\x02 \x01(\tB\x13\xf2\xde\x1f\x0fyaml:"subdenom":&\x8a\xe7\xb0*!osmosis/tokenfactory/create-denom"M\n\x16MsgCreateDenomResponse\x123\n\x0fnew_token_denom\x18\x01 \x01(\tB\x1a\xf2\xde\x1f\x16yaml:"new_token_denom""\xc1\x01\n\x07MsgMint\x12!\n\x06sender\x18\x01 \x01(\tB\x11\xf2\xde\x1f\ryaml:"sender"\x12@\n\x06amount\x18\x02 \x01(\x0b2\x19.cosmos.base.v1beta1.CoinB\x15\xc8\xde\x1f\x00\xf2\xde\x1f\ryaml:"amount"\x121\n\rmintToAddress\x18\x03 \x01(\tB\x1a\xf2\xde\x1f\x16yaml:"mint_to_address":\x1e\x8a\xe7\xb0*\x19osmosis/tokenfactory/mint"\x11\n\x0fMsgMintResponse"\xc5\x01\n\x07MsgBurn\x12!\n\x06sender\x18\x01 \x01(\tB\x11\xf2\xde\x1f\ryaml:"sender"\x12@\n\x06amount\x18\x02 \x01(\x0b2\x19.cosmos.base.v1beta1.CoinB\x15\xc8\xde\x1f\x00\xf2\xde\x1f\ryaml:"amount"\x125\n\x0fburnFromAddress\x18\x03 \x01(\tB\x1c\xf2\xde\x1f\x18yaml:"burn_from_address":\x1e\x8a\xe7\xb0*\x19osmosis/tokenfactory/burn"\x11\n\x0fMsgBurnResponse"\xa5\x01\n\x0eMsgChangeAdmin\x12!\n\x06sender\x18\x01 \x01(\tB\x11\xf2\xde\x1f\ryaml:"sender"\x12\x1f\n\x05denom\x18\x02 \x01(\tB\x10\xf2\xde\x1f\x0cyaml:"denom"\x12\'\n\tnew_admin\x18\x03 \x01(\tB\x14\xf2\xde\x1f\x10yaml:"new_admin":&\x8a\xe7\xb0*!osmosis/tokenfactory/change-admin"\x18\n\x16MsgChangeAdminResponse"\xc0\x01\n\x14MsgSetBeforeSendHook\x12!\n\x06sender\x18\x01 \x01(\tB\x11\xf2\xde\x1f\ryaml:"sender"\x12\x1f\n\x05denom\x18\x02 \x01(\tB\x10\xf2\xde\x1f\x0cyaml:"denom"\x125\n\x10cosmwasm_address\x18\x03 \x01(\tB\x1b\xf2\xde\x1f\x17yaml:"cosmwasm_address":-\x8a\xe7\xb0*(osmosis/tokenfactory/set-beforesend-hook"\x1e\n\x1cMsgSetBeforeSendHookResponse"\x82\x01\n\x13MsgSetDenomMetadata\x12!\n\x06sender\x18\x01 \x01(\tB\x11\xf2\xde\x1f\ryaml:"sender"\x12H\n\x08metadata\x18\x02 \x01(\x0b2\x1d.cosmos.bank.v1beta1.MetadataB\x17\xc8\xde\x1f\x00\xf2\xde\x1f\x0fyaml:"metadata""\x1d\n\x1bMsgSetDenomMetadataResponse"\x9b\x02\n\x10MsgForceTransfer\x12!\n\x06sender\x18\x01 \x01(\tB\x11\xf2\xde\x1f\ryaml:"sender"\x12@\n\x06amount\x18\x02 \x01(\x0b2\x19.cosmos.base.v1beta1.CoinB\x15\xc8\xde\x1f\x00\xf2\xde\x1f\ryaml:"amount"\x12=\n\x13transferFromAddress\x18\x03 \x01(\tB \xf2\xde\x1f\x1cyaml:"transfer_from_address"\x129\n\x11transferToAddress\x18\x04 \x01(\tB\x1e\xf2\xde\x1f\x1ayaml:"transfer_to_address":(\x8a\xe7\xb0*#osmosis/tokenfactory/force-transfer"\x1a\n\x18MsgForceTransferResponse2\xa9\x06\n\x03Msg\x12q\n\x0bCreateDenom\x12,.osmosis.tokenfactory.v1beta1.MsgCreateDenom\x1a4.osmosis.tokenfactory.v1beta1.MsgCreateDenomResponse\x12\\\n\x04Mint\x12%.osmosis.tokenfactory.v1beta1.MsgMint\x1a-.osmosis.tokenfactory.v1beta1.MsgMintResponse\x12\\\n\x04Burn\x12%.osmosis.tokenfactory.v1beta1.MsgBurn\x1a-.osmosis.tokenfactory.v1beta1.MsgBurnResponse\x12q\n\x0bChangeAdmin\x12,.osmosis.tokenfactory.v1beta1.MsgChangeAdmin\x1a4.osmosis.tokenfactory.v1beta1.MsgChangeAdminResponse\x12\x80\x01\n\x10SetDenomMetadata\x121.osmosis.tokenfactory.v1beta1.MsgSetDenomMetadata\x1a9.osmosis.tokenfactory.v1beta1.MsgSetDenomMetadataResponse\x12\x83\x01\n\x11SetBeforeSendHook\x122.osmosis.tokenfactory.v1beta1.MsgSetBeforeSendHook\x1a:.osmosis.tokenfactory.v1beta1.MsgSetBeforeSendHookResponse\x12w\n\rForceTransfer\x12..osmosis.tokenfactory.v1beta1.MsgForceTransfer\x1a6.osmosis.tokenfactory.v1beta1.MsgForceTransferResponseB:Z8github.com/osmosis-labs/osmosis/v21/x/tokenfactory/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.tokenfactory.v1beta1.tx_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z8github.com/osmosis-labs/osmosis/v21/x/tokenfactory/types'
    _MSGCREATEDENOM.fields_by_name['sender']._options = None
    _MSGCREATEDENOM.fields_by_name['sender']._serialized_options = b'\xf2\xde\x1f\ryaml:"sender"'
    _MSGCREATEDENOM.fields_by_name['subdenom']._options = None
    _MSGCREATEDENOM.fields_by_name['subdenom']._serialized_options = b'\xf2\xde\x1f\x0fyaml:"subdenom"'
    _MSGCREATEDENOM._options = None
    _MSGCREATEDENOM._serialized_options = b'\x8a\xe7\xb0*!osmosis/tokenfactory/create-denom'
    _MSGCREATEDENOMRESPONSE.fields_by_name['new_token_denom']._options = None
    _MSGCREATEDENOMRESPONSE.fields_by_name['new_token_denom']._serialized_options = b'\xf2\xde\x1f\x16yaml:"new_token_denom"'
    _MSGMINT.fields_by_name['sender']._options = None
    _MSGMINT.fields_by_name['sender']._serialized_options = b'\xf2\xde\x1f\ryaml:"sender"'
    _MSGMINT.fields_by_name['amount']._options = None
    _MSGMINT.fields_by_name['amount']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\ryaml:"amount"'
    _MSGMINT.fields_by_name['mintToAddress']._options = None
    _MSGMINT.fields_by_name['mintToAddress']._serialized_options = b'\xf2\xde\x1f\x16yaml:"mint_to_address"'
    _MSGMINT._options = None
    _MSGMINT._serialized_options = b'\x8a\xe7\xb0*\x19osmosis/tokenfactory/mint'
    _MSGBURN.fields_by_name['sender']._options = None
    _MSGBURN.fields_by_name['sender']._serialized_options = b'\xf2\xde\x1f\ryaml:"sender"'
    _MSGBURN.fields_by_name['amount']._options = None
    _MSGBURN.fields_by_name['amount']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\ryaml:"amount"'
    _MSGBURN.fields_by_name['burnFromAddress']._options = None
    _MSGBURN.fields_by_name['burnFromAddress']._serialized_options = b'\xf2\xde\x1f\x18yaml:"burn_from_address"'
    _MSGBURN._options = None
    _MSGBURN._serialized_options = b'\x8a\xe7\xb0*\x19osmosis/tokenfactory/burn'
    _MSGCHANGEADMIN.fields_by_name['sender']._options = None
    _MSGCHANGEADMIN.fields_by_name['sender']._serialized_options = b'\xf2\xde\x1f\ryaml:"sender"'
    _MSGCHANGEADMIN.fields_by_name['denom']._options = None
    _MSGCHANGEADMIN.fields_by_name['denom']._serialized_options = b'\xf2\xde\x1f\x0cyaml:"denom"'
    _MSGCHANGEADMIN.fields_by_name['new_admin']._options = None
    _MSGCHANGEADMIN.fields_by_name['new_admin']._serialized_options = b'\xf2\xde\x1f\x10yaml:"new_admin"'
    _MSGCHANGEADMIN._options = None
    _MSGCHANGEADMIN._serialized_options = b'\x8a\xe7\xb0*!osmosis/tokenfactory/change-admin'
    _MSGSETBEFORESENDHOOK.fields_by_name['sender']._options = None
    _MSGSETBEFORESENDHOOK.fields_by_name['sender']._serialized_options = b'\xf2\xde\x1f\ryaml:"sender"'
    _MSGSETBEFORESENDHOOK.fields_by_name['denom']._options = None
    _MSGSETBEFORESENDHOOK.fields_by_name['denom']._serialized_options = b'\xf2\xde\x1f\x0cyaml:"denom"'
    _MSGSETBEFORESENDHOOK.fields_by_name['cosmwasm_address']._options = None
    _MSGSETBEFORESENDHOOK.fields_by_name['cosmwasm_address']._serialized_options = b'\xf2\xde\x1f\x17yaml:"cosmwasm_address"'
    _MSGSETBEFORESENDHOOK._options = None
    _MSGSETBEFORESENDHOOK._serialized_options = b'\x8a\xe7\xb0*(osmosis/tokenfactory/set-beforesend-hook'
    _MSGSETDENOMMETADATA.fields_by_name['sender']._options = None
    _MSGSETDENOMMETADATA.fields_by_name['sender']._serialized_options = b'\xf2\xde\x1f\ryaml:"sender"'
    _MSGSETDENOMMETADATA.fields_by_name['metadata']._options = None
    _MSGSETDENOMMETADATA.fields_by_name['metadata']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x0fyaml:"metadata"'
    _MSGFORCETRANSFER.fields_by_name['sender']._options = None
    _MSGFORCETRANSFER.fields_by_name['sender']._serialized_options = b'\xf2\xde\x1f\ryaml:"sender"'
    _MSGFORCETRANSFER.fields_by_name['amount']._options = None
    _MSGFORCETRANSFER.fields_by_name['amount']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\ryaml:"amount"'
    _MSGFORCETRANSFER.fields_by_name['transferFromAddress']._options = None
    _MSGFORCETRANSFER.fields_by_name['transferFromAddress']._serialized_options = b'\xf2\xde\x1f\x1cyaml:"transfer_from_address"'
    _MSGFORCETRANSFER.fields_by_name['transferToAddress']._options = None
    _MSGFORCETRANSFER.fields_by_name['transferToAddress']._serialized_options = b'\xf2\xde\x1f\x1ayaml:"transfer_to_address"'
    _MSGFORCETRANSFER._options = None
    _MSGFORCETRANSFER._serialized_options = b'\x8a\xe7\xb0*#osmosis/tokenfactory/force-transfer'
    _globals['_MSGCREATEDENOM']._serialized_start = 177
    _globals['_MSGCREATEDENOM']._serialized_end = 307
    _globals['_MSGCREATEDENOMRESPONSE']._serialized_start = 309
    _globals['_MSGCREATEDENOMRESPONSE']._serialized_end = 386
    _globals['_MSGMINT']._serialized_start = 389
    _globals['_MSGMINT']._serialized_end = 582
    _globals['_MSGMINTRESPONSE']._serialized_start = 584
    _globals['_MSGMINTRESPONSE']._serialized_end = 601
    _globals['_MSGBURN']._serialized_start = 604
    _globals['_MSGBURN']._serialized_end = 801
    _globals['_MSGBURNRESPONSE']._serialized_start = 803
    _globals['_MSGBURNRESPONSE']._serialized_end = 820
    _globals['_MSGCHANGEADMIN']._serialized_start = 823
    _globals['_MSGCHANGEADMIN']._serialized_end = 988
    _globals['_MSGCHANGEADMINRESPONSE']._serialized_start = 990
    _globals['_MSGCHANGEADMINRESPONSE']._serialized_end = 1014
    _globals['_MSGSETBEFORESENDHOOK']._serialized_start = 1017
    _globals['_MSGSETBEFORESENDHOOK']._serialized_end = 1209
    _globals['_MSGSETBEFORESENDHOOKRESPONSE']._serialized_start = 1211
    _globals['_MSGSETBEFORESENDHOOKRESPONSE']._serialized_end = 1241
    _globals['_MSGSETDENOMMETADATA']._serialized_start = 1244
    _globals['_MSGSETDENOMMETADATA']._serialized_end = 1374
    _globals['_MSGSETDENOMMETADATARESPONSE']._serialized_start = 1376
    _globals['_MSGSETDENOMMETADATARESPONSE']._serialized_end = 1405
    _globals['_MSGFORCETRANSFER']._serialized_start = 1408
    _globals['_MSGFORCETRANSFER']._serialized_end = 1691
    _globals['_MSGFORCETRANSFERRESPONSE']._serialized_start = 1693
    _globals['_MSGFORCETRANSFERRESPONSE']._serialized_end = 1719
    _globals['_MSG']._serialized_start = 1722
    _globals['_MSG']._serialized_end = 2531