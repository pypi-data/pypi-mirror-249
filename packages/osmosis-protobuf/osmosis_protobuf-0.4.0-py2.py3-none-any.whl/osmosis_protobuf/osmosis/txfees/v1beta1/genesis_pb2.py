"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....osmosis.txfees.v1beta1 import feetoken_pb2 as osmosis_dot_txfees_dot_v1beta1_dot_feetoken__pb2
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$osmosis/txfees/v1beta1/genesis.proto\x12\x16osmosis.txfees.v1beta1\x1a\x14gogoproto/gogo.proto\x1a%osmosis/txfees/v1beta1/feetoken.proto\x1a\x1ecosmos/base/v1beta1/coin.proto"\x9a\x01\n\x0cGenesisState\x12\x11\n\tbasedenom\x18\x01 \x01(\t\x129\n\tfeetokens\x18\x02 \x03(\x0b2 .osmosis.txfees.v1beta1.FeeTokenB\x04\xc8\xde\x1f\x00\x12<\n\rtxFeesTracker\x18\x03 \x01(\x0b2%.osmosis.txfees.v1beta1.TxFeesTracker"\xbe\x01\n\rTxFeesTracker\x12\\\n\x07tx_fees\x18\x01 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x12O\n\x1dheight_accounting_starts_from\x18\x02 \x01(\x03B(\xf2\xde\x1f$yaml:"height_accounting_starts_from"B4Z2github.com/osmosis-labs/osmosis/v21/x/txfees/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.txfees.v1beta1.genesis_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z2github.com/osmosis-labs/osmosis/v21/x/txfees/types'
    _GENESISSTATE.fields_by_name['feetokens']._options = None
    _GENESISSTATE.fields_by_name['feetokens']._serialized_options = b'\xc8\xde\x1f\x00'
    _TXFEESTRACKER.fields_by_name['tx_fees']._options = None
    _TXFEESTRACKER.fields_by_name['tx_fees']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _TXFEESTRACKER.fields_by_name['height_accounting_starts_from']._options = None
    _TXFEESTRACKER.fields_by_name['height_accounting_starts_from']._serialized_options = b'\xf2\xde\x1f$yaml:"height_accounting_starts_from"'
    _globals['_GENESISSTATE']._serialized_start = 158
    _globals['_GENESISSTATE']._serialized_end = 312
    _globals['_TXFEESTRACKER']._serialized_start = 315
    _globals['_TXFEESTRACKER']._serialized_end = 505