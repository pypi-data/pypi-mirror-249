"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....cosmos.crypto.multisig.v1beta1 import multisig_pb2 as cosmos_dot_crypto_dot_multisig_dot_v1beta1_dot_multisig__pb2
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from ....cosmos.tx.signing.v1beta1 import signing_pb2 as cosmos_dot_tx_dot_signing_dot_v1beta1_dot_signing__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1acosmos/tx/v1beta1/tx.proto\x12\x11cosmos.tx.v1beta1\x1a\x14gogoproto/gogo.proto\x1a-cosmos/crypto/multisig/v1beta1/multisig.proto\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a\'cosmos/tx/signing/v1beta1/signing.proto\x1a\x19google/protobuf/any.proto\x1a\x19cosmos_proto/cosmos.proto"q\n\x02Tx\x12\'\n\x04body\x18\x01 \x01(\x0b2\x19.cosmos.tx.v1beta1.TxBody\x12.\n\tauth_info\x18\x02 \x01(\x0b2\x1b.cosmos.tx.v1beta1.AuthInfo\x12\x12\n\nsignatures\x18\x03 \x03(\x0c"H\n\x05TxRaw\x12\x12\n\nbody_bytes\x18\x01 \x01(\x0c\x12\x17\n\x0fauth_info_bytes\x18\x02 \x01(\x0c\x12\x12\n\nsignatures\x18\x03 \x03(\x0c"`\n\x07SignDoc\x12\x12\n\nbody_bytes\x18\x01 \x01(\x0c\x12\x17\n\x0fauth_info_bytes\x18\x02 \x01(\x0c\x12\x10\n\x08chain_id\x18\x03 \x01(\t\x12\x16\n\x0eaccount_number\x18\x04 \x01(\x04"\xb1\x01\n\x10SignDocDirectAux\x12\x12\n\nbody_bytes\x18\x01 \x01(\x0c\x12(\n\npublic_key\x18\x02 \x01(\x0b2\x14.google.protobuf.Any\x12\x10\n\x08chain_id\x18\x03 \x01(\t\x12\x16\n\x0eaccount_number\x18\x04 \x01(\x04\x12\x10\n\x08sequence\x18\x05 \x01(\x04\x12#\n\x03tip\x18\x06 \x01(\x0b2\x16.cosmos.tx.v1beta1.Tip"\xc7\x01\n\x06TxBody\x12&\n\x08messages\x18\x01 \x03(\x0b2\x14.google.protobuf.Any\x12\x0c\n\x04memo\x18\x02 \x01(\t\x12\x16\n\x0etimeout_height\x18\x03 \x01(\x04\x120\n\x11extension_options\x18\xff\x07 \x03(\x0b2\x14.google.protobuf.Any\x12=\n\x1enon_critical_extension_options\x18\xff\x0f \x03(\x0b2\x14.google.protobuf.Any"\x89\x01\n\x08AuthInfo\x123\n\x0csigner_infos\x18\x01 \x03(\x0b2\x1d.cosmos.tx.v1beta1.SignerInfo\x12#\n\x03fee\x18\x02 \x01(\x0b2\x16.cosmos.tx.v1beta1.Fee\x12#\n\x03tip\x18\x03 \x01(\x0b2\x16.cosmos.tx.v1beta1.Tip"x\n\nSignerInfo\x12(\n\npublic_key\x18\x01 \x01(\x0b2\x14.google.protobuf.Any\x12.\n\tmode_info\x18\x02 \x01(\x0b2\x1b.cosmos.tx.v1beta1.ModeInfo\x12\x10\n\x08sequence\x18\x03 \x01(\x04"\xb5\x02\n\x08ModeInfo\x124\n\x06single\x18\x01 \x01(\x0b2".cosmos.tx.v1beta1.ModeInfo.SingleH\x00\x122\n\x05multi\x18\x02 \x01(\x0b2!.cosmos.tx.v1beta1.ModeInfo.MultiH\x00\x1a;\n\x06Single\x121\n\x04mode\x18\x01 \x01(\x0e2#.cosmos.tx.signing.v1beta1.SignMode\x1a{\n\x05Multi\x12A\n\x08bitarray\x18\x01 \x01(\x0b2/.cosmos.crypto.multisig.v1beta1.CompactBitArray\x12/\n\nmode_infos\x18\x02 \x03(\x0b2\x1b.cosmos.tx.v1beta1.ModeInfoB\x05\n\x03sum"\xc9\x01\n\x03Fee\x12[\n\x06amount\x18\x01 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x12\x11\n\tgas_limit\x18\x02 \x01(\x04\x12\'\n\x05payer\x18\x03 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString\x12)\n\x07granter\x18\x04 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString"\x8c\x01\n\x03Tip\x12[\n\x06amount\x18\x01 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x12(\n\x06tipper\x18\x02 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString"\xb1\x01\n\rAuxSignerData\x12)\n\x07address\x18\x01 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString\x125\n\x08sign_doc\x18\x02 \x01(\x0b2#.cosmos.tx.v1beta1.SignDocDirectAux\x121\n\x04mode\x18\x03 \x01(\x0e2#.cosmos.tx.signing.v1beta1.SignMode\x12\x0b\n\x03sig\x18\x04 \x01(\x0cB\'Z%github.com/cosmos/cosmos-sdk/types/txb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.tx.v1beta1.tx_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z%github.com/cosmos/cosmos-sdk/types/tx'
    _FEE.fields_by_name['amount']._options = None
    _FEE.fields_by_name['amount']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _FEE.fields_by_name['payer']._options = None
    _FEE.fields_by_name['payer']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _FEE.fields_by_name['granter']._options = None
    _FEE.fields_by_name['granter']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _TIP.fields_by_name['amount']._options = None
    _TIP.fields_by_name['amount']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _TIP.fields_by_name['tipper']._options = None
    _TIP.fields_by_name['tipper']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _AUXSIGNERDATA.fields_by_name['address']._options = None
    _AUXSIGNERDATA.fields_by_name['address']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _globals['_TX']._serialized_start = 245
    _globals['_TX']._serialized_end = 358
    _globals['_TXRAW']._serialized_start = 360
    _globals['_TXRAW']._serialized_end = 432
    _globals['_SIGNDOC']._serialized_start = 434
    _globals['_SIGNDOC']._serialized_end = 530
    _globals['_SIGNDOCDIRECTAUX']._serialized_start = 533
    _globals['_SIGNDOCDIRECTAUX']._serialized_end = 710
    _globals['_TXBODY']._serialized_start = 713
    _globals['_TXBODY']._serialized_end = 912
    _globals['_AUTHINFO']._serialized_start = 915
    _globals['_AUTHINFO']._serialized_end = 1052
    _globals['_SIGNERINFO']._serialized_start = 1054
    _globals['_SIGNERINFO']._serialized_end = 1174
    _globals['_MODEINFO']._serialized_start = 1177
    _globals['_MODEINFO']._serialized_end = 1486
    _globals['_MODEINFO_SINGLE']._serialized_start = 1295
    _globals['_MODEINFO_SINGLE']._serialized_end = 1354
    _globals['_MODEINFO_MULTI']._serialized_start = 1356
    _globals['_MODEINFO_MULTI']._serialized_end = 1479
    _globals['_FEE']._serialized_start = 1489
    _globals['_FEE']._serialized_end = 1690
    _globals['_TIP']._serialized_start = 1693
    _globals['_TIP']._serialized_end = 1833
    _globals['_AUXSIGNERDATA']._serialized_start = 1836
    _globals['_AUXSIGNERDATA']._serialized_end = 2013