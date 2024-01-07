"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ...gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ...amino import amino_pb2 as amino_dot_amino__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from ...cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from ...osmosis.superfluid import superfluid_pb2 as osmosis_dot_superfluid_dot_superfluid__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1bosmosis/superfluid/tx.proto\x12\x12osmosis.superfluid\x1a\x14gogoproto/gogo.proto\x1a\x11amino/amino.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a#osmosis/superfluid/superfluid.proto"\x7f\n\x15MsgSuperfluidDelegate\x12!\n\x06sender\x18\x01 \x01(\tB\x11\xf2\xde\x1f\ryaml:"sender"\x12\x0f\n\x07lock_id\x18\x02 \x01(\x04\x12\x10\n\x08val_addr\x18\x03 \x01(\t: \x8a\xe7\xb0*\x1bosmosis/superfluid-delegate"\x1f\n\x1dMsgSuperfluidDelegateResponse"q\n\x17MsgSuperfluidUndelegate\x12!\n\x06sender\x18\x01 \x01(\tB\x11\xf2\xde\x1f\ryaml:"sender"\x12\x0f\n\x07lock_id\x18\x02 \x01(\x04:"\x8a\xe7\xb0*\x1dosmosis/superfluid-undelegate"!\n\x1fMsgSuperfluidUndelegateResponse"r\n\x17MsgSuperfluidUnbondLock\x12!\n\x06sender\x18\x01 \x01(\tB\x11\xf2\xde\x1f\ryaml:"sender"\x12\x0f\n\x07lock_id\x18\x02 \x01(\x04:#\x8a\xe7\xb0*\x1eosmosis/superfluid-unbond-lock"!\n\x1fMsgSuperfluidUnbondLockResponse"\x98\x01\n$MsgSuperfluidUndelegateAndUnbondLock\x12!\n\x06sender\x18\x01 \x01(\tB\x11\xf2\xde\x1f\ryaml:"sender"\x12\x0f\n\x07lock_id\x18\x02 \x01(\x04\x12<\n\x04coin\x18\x03 \x01(\x0b2\x19.cosmos.base.v1beta1.CoinB\x13\xc8\xde\x1f\x00\xf2\xde\x1f\x0byaml:"coin""?\n,MsgSuperfluidUndelegateAndUnbondLockResponse\x12\x0f\n\x07lock_id\x18\x01 \x01(\x04"\xda\x01\n\x1cMsgLockAndSuperfluidDelegate\x12!\n\x06sender\x18\x01 \x01(\tB\x11\xf2\xde\x1f\ryaml:"sender"\x12Z\n\x05coins\x18\x02 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x12\x10\n\x08val_addr\x18\x03 \x01(\t:)\x8a\xe7\xb0*$osmosis/lock-and-superfluid-delegate"2\n$MsgLockAndSuperfluidDelegateResponse\x12\n\n\x02ID\x18\x01 \x01(\x04"\x90\x02\n/MsgCreateFullRangePositionAndSuperfluidDelegate\x12!\n\x06sender\x18\x01 \x01(\tB\x11\xf2\xde\x1f\ryaml:"sender"\x12Z\n\x05coins\x18\x02 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x12\x10\n\x08val_addr\x18\x03 \x01(\t\x12#\n\x07pool_id\x18\x04 \x01(\x04B\x12\xf2\xde\x1f\x0eyaml:"pool_id":\'\x8a\xe7\xb0*"osmosis/full-range-and-sf-delegate"]\n7MsgCreateFullRangePositionAndSuperfluidDelegateResponse\x12\x0e\n\x06lockID\x18\x01 \x01(\x04\x12\x12\n\npositionID\x18\x02 \x01(\x04"\x88\x01\n\x18MsgUnPoolWhitelistedPool\x12!\n\x06sender\x18\x01 \x01(\tB\x11\xf2\xde\x1f\ryaml:"sender"\x12#\n\x07pool_id\x18\x02 \x01(\x04B\x12\xf2\xde\x1f\x0eyaml:"pool_id":$\x8a\xe7\xb0*\x1fosmosis/unpool-whitelisted-pool";\n MsgUnPoolWhitelistedPoolResponse\x12\x17\n\x0fexited_lock_ids\x18\x01 \x03(\x04"\xf9\x02\n8MsgUnlockAndMigrateSharesToFullRangeConcentratedPosition\x12!\n\x06sender\x18\x01 \x01(\tB\x11\xf2\xde\x1f\ryaml:"sender"\x12#\n\x07lock_id\x18\x02 \x01(\x03B\x12\xf2\xde\x1f\x0eyaml:"lock_id"\x12V\n\x11shares_to_migrate\x18\x03 \x01(\x0b2\x19.cosmos.base.v1beta1.CoinB \xc8\xde\x1f\x00\xf2\xde\x1f\x18yaml:"shares_to_migrate"\x12|\n\x0etoken_out_mins\x18\x04 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinBI\xc8\xde\x1f\x00\xf2\xde\x1f\x15yaml:"token_out_mins"\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins:\x1f\x8a\xe7\xb0*\x1aosmosis/unlock-and-migrate"\xef\x02\n@MsgUnlockAndMigrateSharesToFullRangeConcentratedPositionResponse\x12@\n\x07amount0\x18\x01 \x01(\tB/\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x0eyaml:"amount0"\x12@\n\x07amount1\x18\x02 \x01(\tB/\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x0eyaml:"amount1"\x12Z\n\x11liquidity_created\x18\x03 \x01(\tB?\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x18yaml:"liquidity_created"\x12K\n\tjoin_time\x18\x04 \x01(\x0b2\x1a.google.protobuf.TimestampB\x1c\xc8\xde\x1f\x00\xf2\xde\x1f\x10yaml:"join_time"\x90\xdf\x1f\x01"\xd1\x02\n/MsgAddToConcentratedLiquiditySuperfluidPosition\x12+\n\x0bposition_id\x18\x01 \x01(\x04B\x16\xf2\xde\x1f\x12yaml:"position_id"\x12!\n\x06sender\x18\x02 \x01(\tB\x11\xf2\xde\x1f\ryaml:"sender"\x12P\n\x0etoken_desired0\x18\x03 \x01(\x0b2\x19.cosmos.base.v1beta1.CoinB\x1d\xc8\xde\x1f\x00\xf2\xde\x1f\x15yaml:"token_desired0"\x12P\n\x0etoken_desired1\x18\x04 \x01(\x0b2\x19.cosmos.base.v1beta1.CoinB\x1d\xc8\xde\x1f\x00\xf2\xde\x1f\x15yaml:"token_desired1":*\x8a\xe7\xb0*%osmosis/add-to-cl-superfluid-position"\xe3\x02\n7MsgAddToConcentratedLiquiditySuperfluidPositionResponse\x12+\n\x0bposition_id\x18\x01 \x01(\x04B\x16\xf2\xde\x1f\x12yaml:"position_id"\x12@\n\x07amount0\x18\x02 \x01(\tB/\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x0eyaml:"amount0"\x12@\n\x07amount1\x18\x03 \x01(\tB/\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x0eyaml:"amount1"\x12R\n\rnew_liquidity\x18\x05 \x01(\tB;\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x14yaml:"new_liquidity"\x12#\n\x07lock_id\x18\x04 \x01(\x04B\x12\xf2\xde\x1f\x0eyaml:"lock_id""\xf3\x02\n\x18MsgUnbondConvertAndStake\x12#\n\x07lock_id\x18\x01 \x01(\x04B\x12\xf2\xde\x1f\x0eyaml:"lock_id"\x12!\n\x06sender\x18\x02 \x01(\tB\x11\xf2\xde\x1f\ryaml:"sender"\x12\x10\n\x08val_addr\x18\x03 \x01(\t\x12R\n\x10min_amt_to_stake\x18\x04 \x01(\tB8\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x17yaml:"min_amt_to_stake"\x12\x81\x01\n\x11shares_to_convert\x18\x05 \x01(\x0b2\x19.cosmos.base.v1beta1.CoinBK\xc8\xde\x1f\x00\xf2\xde\x1f\x18yaml:"shares_to_convert"\xaa\xdf\x1f\'github.com/cosmos/cosmos-sdk/types.Coin:%\x8a\xe7\xb0* osmosis/unbond-convert-and-stake"v\n MsgUnbondConvertAndStakeResponse\x12R\n\x10total_amt_staked\x18\x01 \x01(\tB8\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x17yaml:"total_amt_staked"2\xf7\x0b\n\x03Msg\x12r\n\x12SuperfluidDelegate\x12).osmosis.superfluid.MsgSuperfluidDelegate\x1a1.osmosis.superfluid.MsgSuperfluidDelegateResponse\x12x\n\x14SuperfluidUndelegate\x12+.osmosis.superfluid.MsgSuperfluidUndelegate\x1a3.osmosis.superfluid.MsgSuperfluidUndelegateResponse\x12x\n\x14SuperfluidUnbondLock\x12+.osmosis.superfluid.MsgSuperfluidUnbondLock\x1a3.osmosis.superfluid.MsgSuperfluidUnbondLockResponse\x12\x9f\x01\n!SuperfluidUndelegateAndUnbondLock\x128.osmosis.superfluid.MsgSuperfluidUndelegateAndUnbondLock\x1a@.osmosis.superfluid.MsgSuperfluidUndelegateAndUnbondLockResponse\x12\x87\x01\n\x19LockAndSuperfluidDelegate\x120.osmosis.superfluid.MsgLockAndSuperfluidDelegate\x1a8.osmosis.superfluid.MsgLockAndSuperfluidDelegateResponse\x12\xc0\x01\n,CreateFullRangePositionAndSuperfluidDelegate\x12C.osmosis.superfluid.MsgCreateFullRangePositionAndSuperfluidDelegate\x1aK.osmosis.superfluid.MsgCreateFullRangePositionAndSuperfluidDelegateResponse\x12{\n\x15UnPoolWhitelistedPool\x12,.osmosis.superfluid.MsgUnPoolWhitelistedPool\x1a4.osmosis.superfluid.MsgUnPoolWhitelistedPoolResponse\x12\xdb\x01\n5UnlockAndMigrateSharesToFullRangeConcentratedPosition\x12L.osmosis.superfluid.MsgUnlockAndMigrateSharesToFullRangeConcentratedPosition\x1aT.osmosis.superfluid.MsgUnlockAndMigrateSharesToFullRangeConcentratedPositionResponse\x12\xc0\x01\n,AddToConcentratedLiquiditySuperfluidPosition\x12C.osmosis.superfluid.MsgAddToConcentratedLiquiditySuperfluidPosition\x1aK.osmosis.superfluid.MsgAddToConcentratedLiquiditySuperfluidPositionResponse\x12{\n\x15UnbondConvertAndStake\x12,.osmosis.superfluid.MsgUnbondConvertAndStake\x1a4.osmosis.superfluid.MsgUnbondConvertAndStakeResponseB8Z6github.com/osmosis-labs/osmosis/v21/x/superfluid/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.superfluid.tx_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z6github.com/osmosis-labs/osmosis/v21/x/superfluid/types'
    _MSGSUPERFLUIDDELEGATE.fields_by_name['sender']._options = None
    _MSGSUPERFLUIDDELEGATE.fields_by_name['sender']._serialized_options = b'\xf2\xde\x1f\ryaml:"sender"'
    _MSGSUPERFLUIDDELEGATE._options = None
    _MSGSUPERFLUIDDELEGATE._serialized_options = b'\x8a\xe7\xb0*\x1bosmosis/superfluid-delegate'
    _MSGSUPERFLUIDUNDELEGATE.fields_by_name['sender']._options = None
    _MSGSUPERFLUIDUNDELEGATE.fields_by_name['sender']._serialized_options = b'\xf2\xde\x1f\ryaml:"sender"'
    _MSGSUPERFLUIDUNDELEGATE._options = None
    _MSGSUPERFLUIDUNDELEGATE._serialized_options = b'\x8a\xe7\xb0*\x1dosmosis/superfluid-undelegate'
    _MSGSUPERFLUIDUNBONDLOCK.fields_by_name['sender']._options = None
    _MSGSUPERFLUIDUNBONDLOCK.fields_by_name['sender']._serialized_options = b'\xf2\xde\x1f\ryaml:"sender"'
    _MSGSUPERFLUIDUNBONDLOCK._options = None
    _MSGSUPERFLUIDUNBONDLOCK._serialized_options = b'\x8a\xe7\xb0*\x1eosmosis/superfluid-unbond-lock'
    _MSGSUPERFLUIDUNDELEGATEANDUNBONDLOCK.fields_by_name['sender']._options = None
    _MSGSUPERFLUIDUNDELEGATEANDUNBONDLOCK.fields_by_name['sender']._serialized_options = b'\xf2\xde\x1f\ryaml:"sender"'
    _MSGSUPERFLUIDUNDELEGATEANDUNBONDLOCK.fields_by_name['coin']._options = None
    _MSGSUPERFLUIDUNDELEGATEANDUNBONDLOCK.fields_by_name['coin']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x0byaml:"coin"'
    _MSGLOCKANDSUPERFLUIDDELEGATE.fields_by_name['sender']._options = None
    _MSGLOCKANDSUPERFLUIDDELEGATE.fields_by_name['sender']._serialized_options = b'\xf2\xde\x1f\ryaml:"sender"'
    _MSGLOCKANDSUPERFLUIDDELEGATE.fields_by_name['coins']._options = None
    _MSGLOCKANDSUPERFLUIDDELEGATE.fields_by_name['coins']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _MSGLOCKANDSUPERFLUIDDELEGATE._options = None
    _MSGLOCKANDSUPERFLUIDDELEGATE._serialized_options = b'\x8a\xe7\xb0*$osmosis/lock-and-superfluid-delegate'
    _MSGCREATEFULLRANGEPOSITIONANDSUPERFLUIDDELEGATE.fields_by_name['sender']._options = None
    _MSGCREATEFULLRANGEPOSITIONANDSUPERFLUIDDELEGATE.fields_by_name['sender']._serialized_options = b'\xf2\xde\x1f\ryaml:"sender"'
    _MSGCREATEFULLRANGEPOSITIONANDSUPERFLUIDDELEGATE.fields_by_name['coins']._options = None
    _MSGCREATEFULLRANGEPOSITIONANDSUPERFLUIDDELEGATE.fields_by_name['coins']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _MSGCREATEFULLRANGEPOSITIONANDSUPERFLUIDDELEGATE.fields_by_name['pool_id']._options = None
    _MSGCREATEFULLRANGEPOSITIONANDSUPERFLUIDDELEGATE.fields_by_name['pool_id']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"pool_id"'
    _MSGCREATEFULLRANGEPOSITIONANDSUPERFLUIDDELEGATE._options = None
    _MSGCREATEFULLRANGEPOSITIONANDSUPERFLUIDDELEGATE._serialized_options = b'\x8a\xe7\xb0*"osmosis/full-range-and-sf-delegate'
    _MSGUNPOOLWHITELISTEDPOOL.fields_by_name['sender']._options = None
    _MSGUNPOOLWHITELISTEDPOOL.fields_by_name['sender']._serialized_options = b'\xf2\xde\x1f\ryaml:"sender"'
    _MSGUNPOOLWHITELISTEDPOOL.fields_by_name['pool_id']._options = None
    _MSGUNPOOLWHITELISTEDPOOL.fields_by_name['pool_id']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"pool_id"'
    _MSGUNPOOLWHITELISTEDPOOL._options = None
    _MSGUNPOOLWHITELISTEDPOOL._serialized_options = b'\x8a\xe7\xb0*\x1fosmosis/unpool-whitelisted-pool'
    _MSGUNLOCKANDMIGRATESHARESTOFULLRANGECONCENTRATEDPOSITION.fields_by_name['sender']._options = None
    _MSGUNLOCKANDMIGRATESHARESTOFULLRANGECONCENTRATEDPOSITION.fields_by_name['sender']._serialized_options = b'\xf2\xde\x1f\ryaml:"sender"'
    _MSGUNLOCKANDMIGRATESHARESTOFULLRANGECONCENTRATEDPOSITION.fields_by_name['lock_id']._options = None
    _MSGUNLOCKANDMIGRATESHARESTOFULLRANGECONCENTRATEDPOSITION.fields_by_name['lock_id']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"lock_id"'
    _MSGUNLOCKANDMIGRATESHARESTOFULLRANGECONCENTRATEDPOSITION.fields_by_name['shares_to_migrate']._options = None
    _MSGUNLOCKANDMIGRATESHARESTOFULLRANGECONCENTRATEDPOSITION.fields_by_name['shares_to_migrate']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x18yaml:"shares_to_migrate"'
    _MSGUNLOCKANDMIGRATESHARESTOFULLRANGECONCENTRATEDPOSITION.fields_by_name['token_out_mins']._options = None
    _MSGUNLOCKANDMIGRATESHARESTOFULLRANGECONCENTRATEDPOSITION.fields_by_name['token_out_mins']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x15yaml:"token_out_mins"\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _MSGUNLOCKANDMIGRATESHARESTOFULLRANGECONCENTRATEDPOSITION._options = None
    _MSGUNLOCKANDMIGRATESHARESTOFULLRANGECONCENTRATEDPOSITION._serialized_options = b'\x8a\xe7\xb0*\x1aosmosis/unlock-and-migrate'
    _MSGUNLOCKANDMIGRATESHARESTOFULLRANGECONCENTRATEDPOSITIONRESPONSE.fields_by_name['amount0']._options = None
    _MSGUNLOCKANDMIGRATESHARESTOFULLRANGECONCENTRATEDPOSITIONRESPONSE.fields_by_name['amount0']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x0eyaml:"amount0"'
    _MSGUNLOCKANDMIGRATESHARESTOFULLRANGECONCENTRATEDPOSITIONRESPONSE.fields_by_name['amount1']._options = None
    _MSGUNLOCKANDMIGRATESHARESTOFULLRANGECONCENTRATEDPOSITIONRESPONSE.fields_by_name['amount1']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x0eyaml:"amount1"'
    _MSGUNLOCKANDMIGRATESHARESTOFULLRANGECONCENTRATEDPOSITIONRESPONSE.fields_by_name['liquidity_created']._options = None
    _MSGUNLOCKANDMIGRATESHARESTOFULLRANGECONCENTRATEDPOSITIONRESPONSE.fields_by_name['liquidity_created']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x18yaml:"liquidity_created"'
    _MSGUNLOCKANDMIGRATESHARESTOFULLRANGECONCENTRATEDPOSITIONRESPONSE.fields_by_name['join_time']._options = None
    _MSGUNLOCKANDMIGRATESHARESTOFULLRANGECONCENTRATEDPOSITIONRESPONSE.fields_by_name['join_time']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x10yaml:"join_time"\x90\xdf\x1f\x01'
    _MSGADDTOCONCENTRATEDLIQUIDITYSUPERFLUIDPOSITION.fields_by_name['position_id']._options = None
    _MSGADDTOCONCENTRATEDLIQUIDITYSUPERFLUIDPOSITION.fields_by_name['position_id']._serialized_options = b'\xf2\xde\x1f\x12yaml:"position_id"'
    _MSGADDTOCONCENTRATEDLIQUIDITYSUPERFLUIDPOSITION.fields_by_name['sender']._options = None
    _MSGADDTOCONCENTRATEDLIQUIDITYSUPERFLUIDPOSITION.fields_by_name['sender']._serialized_options = b'\xf2\xde\x1f\ryaml:"sender"'
    _MSGADDTOCONCENTRATEDLIQUIDITYSUPERFLUIDPOSITION.fields_by_name['token_desired0']._options = None
    _MSGADDTOCONCENTRATEDLIQUIDITYSUPERFLUIDPOSITION.fields_by_name['token_desired0']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x15yaml:"token_desired0"'
    _MSGADDTOCONCENTRATEDLIQUIDITYSUPERFLUIDPOSITION.fields_by_name['token_desired1']._options = None
    _MSGADDTOCONCENTRATEDLIQUIDITYSUPERFLUIDPOSITION.fields_by_name['token_desired1']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x15yaml:"token_desired1"'
    _MSGADDTOCONCENTRATEDLIQUIDITYSUPERFLUIDPOSITION._options = None
    _MSGADDTOCONCENTRATEDLIQUIDITYSUPERFLUIDPOSITION._serialized_options = b'\x8a\xe7\xb0*%osmosis/add-to-cl-superfluid-position'
    _MSGADDTOCONCENTRATEDLIQUIDITYSUPERFLUIDPOSITIONRESPONSE.fields_by_name['position_id']._options = None
    _MSGADDTOCONCENTRATEDLIQUIDITYSUPERFLUIDPOSITIONRESPONSE.fields_by_name['position_id']._serialized_options = b'\xf2\xde\x1f\x12yaml:"position_id"'
    _MSGADDTOCONCENTRATEDLIQUIDITYSUPERFLUIDPOSITIONRESPONSE.fields_by_name['amount0']._options = None
    _MSGADDTOCONCENTRATEDLIQUIDITYSUPERFLUIDPOSITIONRESPONSE.fields_by_name['amount0']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x0eyaml:"amount0"'
    _MSGADDTOCONCENTRATEDLIQUIDITYSUPERFLUIDPOSITIONRESPONSE.fields_by_name['amount1']._options = None
    _MSGADDTOCONCENTRATEDLIQUIDITYSUPERFLUIDPOSITIONRESPONSE.fields_by_name['amount1']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x0eyaml:"amount1"'
    _MSGADDTOCONCENTRATEDLIQUIDITYSUPERFLUIDPOSITIONRESPONSE.fields_by_name['new_liquidity']._options = None
    _MSGADDTOCONCENTRATEDLIQUIDITYSUPERFLUIDPOSITIONRESPONSE.fields_by_name['new_liquidity']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x1bcosmossdk.io/math.LegacyDec\xf2\xde\x1f\x14yaml:"new_liquidity"'
    _MSGADDTOCONCENTRATEDLIQUIDITYSUPERFLUIDPOSITIONRESPONSE.fields_by_name['lock_id']._options = None
    _MSGADDTOCONCENTRATEDLIQUIDITYSUPERFLUIDPOSITIONRESPONSE.fields_by_name['lock_id']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"lock_id"'
    _MSGUNBONDCONVERTANDSTAKE.fields_by_name['lock_id']._options = None
    _MSGUNBONDCONVERTANDSTAKE.fields_by_name['lock_id']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"lock_id"'
    _MSGUNBONDCONVERTANDSTAKE.fields_by_name['sender']._options = None
    _MSGUNBONDCONVERTANDSTAKE.fields_by_name['sender']._serialized_options = b'\xf2\xde\x1f\ryaml:"sender"'
    _MSGUNBONDCONVERTANDSTAKE.fields_by_name['min_amt_to_stake']._options = None
    _MSGUNBONDCONVERTANDSTAKE.fields_by_name['min_amt_to_stake']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x17yaml:"min_amt_to_stake"'
    _MSGUNBONDCONVERTANDSTAKE.fields_by_name['shares_to_convert']._options = None
    _MSGUNBONDCONVERTANDSTAKE.fields_by_name['shares_to_convert']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x18yaml:"shares_to_convert"\xaa\xdf\x1f\'github.com/cosmos/cosmos-sdk/types.Coin'
    _MSGUNBONDCONVERTANDSTAKE._options = None
    _MSGUNBONDCONVERTANDSTAKE._serialized_options = b'\x8a\xe7\xb0* osmosis/unbond-convert-and-stake'
    _MSGUNBONDCONVERTANDSTAKERESPONSE.fields_by_name['total_amt_staked']._options = None
    _MSGUNBONDCONVERTANDSTAKERESPONSE.fields_by_name['total_amt_staked']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x15cosmossdk.io/math.Int\xf2\xde\x1f\x17yaml:"total_amt_staked"'
    _globals['_MSGSUPERFLUIDDELEGATE']._serialized_start = 226
    _globals['_MSGSUPERFLUIDDELEGATE']._serialized_end = 353
    _globals['_MSGSUPERFLUIDDELEGATERESPONSE']._serialized_start = 355
    _globals['_MSGSUPERFLUIDDELEGATERESPONSE']._serialized_end = 386
    _globals['_MSGSUPERFLUIDUNDELEGATE']._serialized_start = 388
    _globals['_MSGSUPERFLUIDUNDELEGATE']._serialized_end = 501
    _globals['_MSGSUPERFLUIDUNDELEGATERESPONSE']._serialized_start = 503
    _globals['_MSGSUPERFLUIDUNDELEGATERESPONSE']._serialized_end = 536
    _globals['_MSGSUPERFLUIDUNBONDLOCK']._serialized_start = 538
    _globals['_MSGSUPERFLUIDUNBONDLOCK']._serialized_end = 652
    _globals['_MSGSUPERFLUIDUNBONDLOCKRESPONSE']._serialized_start = 654
    _globals['_MSGSUPERFLUIDUNBONDLOCKRESPONSE']._serialized_end = 687
    _globals['_MSGSUPERFLUIDUNDELEGATEANDUNBONDLOCK']._serialized_start = 690
    _globals['_MSGSUPERFLUIDUNDELEGATEANDUNBONDLOCK']._serialized_end = 842
    _globals['_MSGSUPERFLUIDUNDELEGATEANDUNBONDLOCKRESPONSE']._serialized_start = 844
    _globals['_MSGSUPERFLUIDUNDELEGATEANDUNBONDLOCKRESPONSE']._serialized_end = 907
    _globals['_MSGLOCKANDSUPERFLUIDDELEGATE']._serialized_start = 910
    _globals['_MSGLOCKANDSUPERFLUIDDELEGATE']._serialized_end = 1128
    _globals['_MSGLOCKANDSUPERFLUIDDELEGATERESPONSE']._serialized_start = 1130
    _globals['_MSGLOCKANDSUPERFLUIDDELEGATERESPONSE']._serialized_end = 1180
    _globals['_MSGCREATEFULLRANGEPOSITIONANDSUPERFLUIDDELEGATE']._serialized_start = 1183
    _globals['_MSGCREATEFULLRANGEPOSITIONANDSUPERFLUIDDELEGATE']._serialized_end = 1455
    _globals['_MSGCREATEFULLRANGEPOSITIONANDSUPERFLUIDDELEGATERESPONSE']._serialized_start = 1457
    _globals['_MSGCREATEFULLRANGEPOSITIONANDSUPERFLUIDDELEGATERESPONSE']._serialized_end = 1550
    _globals['_MSGUNPOOLWHITELISTEDPOOL']._serialized_start = 1553
    _globals['_MSGUNPOOLWHITELISTEDPOOL']._serialized_end = 1689
    _globals['_MSGUNPOOLWHITELISTEDPOOLRESPONSE']._serialized_start = 1691
    _globals['_MSGUNPOOLWHITELISTEDPOOLRESPONSE']._serialized_end = 1750
    _globals['_MSGUNLOCKANDMIGRATESHARESTOFULLRANGECONCENTRATEDPOSITION']._serialized_start = 1753
    _globals['_MSGUNLOCKANDMIGRATESHARESTOFULLRANGECONCENTRATEDPOSITION']._serialized_end = 2130
    _globals['_MSGUNLOCKANDMIGRATESHARESTOFULLRANGECONCENTRATEDPOSITIONRESPONSE']._serialized_start = 2133
    _globals['_MSGUNLOCKANDMIGRATESHARESTOFULLRANGECONCENTRATEDPOSITIONRESPONSE']._serialized_end = 2500
    _globals['_MSGADDTOCONCENTRATEDLIQUIDITYSUPERFLUIDPOSITION']._serialized_start = 2503
    _globals['_MSGADDTOCONCENTRATEDLIQUIDITYSUPERFLUIDPOSITION']._serialized_end = 2840
    _globals['_MSGADDTOCONCENTRATEDLIQUIDITYSUPERFLUIDPOSITIONRESPONSE']._serialized_start = 2843
    _globals['_MSGADDTOCONCENTRATEDLIQUIDITYSUPERFLUIDPOSITIONRESPONSE']._serialized_end = 3198
    _globals['_MSGUNBONDCONVERTANDSTAKE']._serialized_start = 3201
    _globals['_MSGUNBONDCONVERTANDSTAKE']._serialized_end = 3572
    _globals['_MSGUNBONDCONVERTANDSTAKERESPONSE']._serialized_start = 3574
    _globals['_MSGUNBONDCONVERTANDSTAKERESPONSE']._serialized_end = 3692
    _globals['_MSG']._serialized_start = 3695
    _globals['_MSG']._serialized_end = 5222