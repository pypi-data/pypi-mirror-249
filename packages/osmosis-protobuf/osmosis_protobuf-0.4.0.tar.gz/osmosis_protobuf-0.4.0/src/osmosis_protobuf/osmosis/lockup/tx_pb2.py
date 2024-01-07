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
from ...osmosis.lockup import lock_pb2 as osmosis_dot_lockup_dot_lock__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17osmosis/lockup/tx.proto\x12\x0eosmosis.lockup\x1a\x14gogoproto/gogo.proto\x1a\x11amino/amino.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a\x19osmosis/lockup/lock.proto"\x8d\x02\n\rMsgLockTokens\x12\x1f\n\x05owner\x18\x01 \x01(\tB\x10\xf2\xde\x1f\x0cyaml:"owner"\x12^\n\x08duration\x18\x02 \x01(\x0b2\x19.google.protobuf.DurationB1\xc8\xde\x1f\x00\xea\xde\x1f\x12duration,omitempty\xf2\xde\x1f\x0fyaml:"duration"\x98\xdf\x1f\x01\x12Z\n\x05coins\x18\x03 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins:\x1f\x8a\xe7\xb0*\x1aosmosis/lockup/lock-tokens"#\n\x15MsgLockTokensResponse\x12\n\n\x02ID\x18\x01 \x01(\x04"`\n\x14MsgBeginUnlockingAll\x12\x1f\n\x05owner\x18\x01 \x01(\tB\x10\xf2\xde\x1f\x0cyaml:"owner":\'\x8a\xe7\xb0*"osmosis/lockup/begin-unlock-tokens"K\n\x1cMsgBeginUnlockingAllResponse\x12+\n\x07unlocks\x18\x01 \x03(\x0b2\x1a.osmosis.lockup.PeriodLock"\xca\x01\n\x11MsgBeginUnlocking\x12\x1f\n\x05owner\x18\x01 \x01(\tB\x10\xf2\xde\x1f\x0cyaml:"owner"\x12\n\n\x02ID\x18\x02 \x01(\x04\x12Z\n\x05coins\x18\x03 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins:,\x8a\xe7\xb0*\'osmosis/lockup/begin-unlock-period-lock"E\n\x19MsgBeginUnlockingResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x17\n\x0funlockingLockID\x18\x02 \x01(\x04"\xc1\x01\n\x0fMsgExtendLockup\x12\x1f\n\x05owner\x18\x01 \x01(\tB\x10\xf2\xde\x1f\x0cyaml:"owner"\x12\n\n\x02ID\x18\x02 \x01(\x04\x12^\n\x08duration\x18\x03 \x01(\x0b2\x19.google.protobuf.DurationB1\xc8\xde\x1f\x00\xea\xde\x1f\x12duration,omitempty\xf2\xde\x1f\x0fyaml:"duration"\x98\xdf\x1f\x01:!\x8a\xe7\xb0*\x1cosmosis/lockup/extend-lockup"*\n\x17MsgExtendLockupResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08"\xc2\x01\n\x0eMsgForceUnlock\x12\x1f\n\x05owner\x18\x01 \x01(\tB\x10\xf2\xde\x1f\x0cyaml:"owner"\x12\n\n\x02ID\x18\x02 \x01(\x04\x12Z\n\x05coins\x18\x03 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins:\'\x8a\xe7\xb0*"osmosis/lockup/force-unlock-tokens")\n\x16MsgForceUnlockResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08"\xb4\x01\n\x1bMsgSetRewardReceiverAddress\x12\x1f\n\x05owner\x18\x01 \x01(\tB\x10\xf2\xde\x1f\x0cyaml:"owner"\x12\x0e\n\x06lockID\x18\x02 \x01(\x04\x123\n\x0freward_receiver\x18\x03 \x01(\tB\x1a\xf2\xde\x1f\x16yaml:"reward_receiver":/\x8a\xe7\xb0**osmosis/lockup/set-reward-receiver-address"6\n#MsgSetRewardReceiverAddressResponse\x12\x0f\n\x07success\x18\x01 \x01(\x082\xd1\x04\n\x03Msg\x12R\n\nLockTokens\x12\x1d.osmosis.lockup.MsgLockTokens\x1a%.osmosis.lockup.MsgLockTokensResponse\x12g\n\x11BeginUnlockingAll\x12$.osmosis.lockup.MsgBeginUnlockingAll\x1a,.osmosis.lockup.MsgBeginUnlockingAllResponse\x12^\n\x0eBeginUnlocking\x12!.osmosis.lockup.MsgBeginUnlocking\x1a).osmosis.lockup.MsgBeginUnlockingResponse\x12X\n\x0cExtendLockup\x12\x1f.osmosis.lockup.MsgExtendLockup\x1a\'.osmosis.lockup.MsgExtendLockupResponse\x12U\n\x0bForceUnlock\x12\x1e.osmosis.lockup.MsgForceUnlock\x1a&.osmosis.lockup.MsgForceUnlockResponse\x12|\n\x18SetRewardReceiverAddress\x12+.osmosis.lockup.MsgSetRewardReceiverAddress\x1a3.osmosis.lockup.MsgSetRewardReceiverAddressResponseB4Z2github.com/osmosis-labs/osmosis/v21/x/lockup/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.lockup.tx_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z2github.com/osmosis-labs/osmosis/v21/x/lockup/types'
    _MSGLOCKTOKENS.fields_by_name['owner']._options = None
    _MSGLOCKTOKENS.fields_by_name['owner']._serialized_options = b'\xf2\xde\x1f\x0cyaml:"owner"'
    _MSGLOCKTOKENS.fields_by_name['duration']._options = None
    _MSGLOCKTOKENS.fields_by_name['duration']._serialized_options = b'\xc8\xde\x1f\x00\xea\xde\x1f\x12duration,omitempty\xf2\xde\x1f\x0fyaml:"duration"\x98\xdf\x1f\x01'
    _MSGLOCKTOKENS.fields_by_name['coins']._options = None
    _MSGLOCKTOKENS.fields_by_name['coins']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _MSGLOCKTOKENS._options = None
    _MSGLOCKTOKENS._serialized_options = b'\x8a\xe7\xb0*\x1aosmosis/lockup/lock-tokens'
    _MSGBEGINUNLOCKINGALL.fields_by_name['owner']._options = None
    _MSGBEGINUNLOCKINGALL.fields_by_name['owner']._serialized_options = b'\xf2\xde\x1f\x0cyaml:"owner"'
    _MSGBEGINUNLOCKINGALL._options = None
    _MSGBEGINUNLOCKINGALL._serialized_options = b'\x8a\xe7\xb0*"osmosis/lockup/begin-unlock-tokens'
    _MSGBEGINUNLOCKING.fields_by_name['owner']._options = None
    _MSGBEGINUNLOCKING.fields_by_name['owner']._serialized_options = b'\xf2\xde\x1f\x0cyaml:"owner"'
    _MSGBEGINUNLOCKING.fields_by_name['coins']._options = None
    _MSGBEGINUNLOCKING.fields_by_name['coins']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _MSGBEGINUNLOCKING._options = None
    _MSGBEGINUNLOCKING._serialized_options = b"\x8a\xe7\xb0*'osmosis/lockup/begin-unlock-period-lock"
    _MSGEXTENDLOCKUP.fields_by_name['owner']._options = None
    _MSGEXTENDLOCKUP.fields_by_name['owner']._serialized_options = b'\xf2\xde\x1f\x0cyaml:"owner"'
    _MSGEXTENDLOCKUP.fields_by_name['duration']._options = None
    _MSGEXTENDLOCKUP.fields_by_name['duration']._serialized_options = b'\xc8\xde\x1f\x00\xea\xde\x1f\x12duration,omitempty\xf2\xde\x1f\x0fyaml:"duration"\x98\xdf\x1f\x01'
    _MSGEXTENDLOCKUP._options = None
    _MSGEXTENDLOCKUP._serialized_options = b'\x8a\xe7\xb0*\x1cosmosis/lockup/extend-lockup'
    _MSGFORCEUNLOCK.fields_by_name['owner']._options = None
    _MSGFORCEUNLOCK.fields_by_name['owner']._serialized_options = b'\xf2\xde\x1f\x0cyaml:"owner"'
    _MSGFORCEUNLOCK.fields_by_name['coins']._options = None
    _MSGFORCEUNLOCK.fields_by_name['coins']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _MSGFORCEUNLOCK._options = None
    _MSGFORCEUNLOCK._serialized_options = b'\x8a\xe7\xb0*"osmosis/lockup/force-unlock-tokens'
    _MSGSETREWARDRECEIVERADDRESS.fields_by_name['owner']._options = None
    _MSGSETREWARDRECEIVERADDRESS.fields_by_name['owner']._serialized_options = b'\xf2\xde\x1f\x0cyaml:"owner"'
    _MSGSETREWARDRECEIVERADDRESS.fields_by_name['reward_receiver']._options = None
    _MSGSETREWARDRECEIVERADDRESS.fields_by_name['reward_receiver']._serialized_options = b'\xf2\xde\x1f\x16yaml:"reward_receiver"'
    _MSGSETREWARDRECEIVERADDRESS._options = None
    _MSGSETREWARDRECEIVERADDRESS._serialized_options = b'\x8a\xe7\xb0**osmosis/lockup/set-reward-receiver-address'
    _globals['_MSGLOCKTOKENS']._serialized_start = 176
    _globals['_MSGLOCKTOKENS']._serialized_end = 445
    _globals['_MSGLOCKTOKENSRESPONSE']._serialized_start = 447
    _globals['_MSGLOCKTOKENSRESPONSE']._serialized_end = 482
    _globals['_MSGBEGINUNLOCKINGALL']._serialized_start = 484
    _globals['_MSGBEGINUNLOCKINGALL']._serialized_end = 580
    _globals['_MSGBEGINUNLOCKINGALLRESPONSE']._serialized_start = 582
    _globals['_MSGBEGINUNLOCKINGALLRESPONSE']._serialized_end = 657
    _globals['_MSGBEGINUNLOCKING']._serialized_start = 660
    _globals['_MSGBEGINUNLOCKING']._serialized_end = 862
    _globals['_MSGBEGINUNLOCKINGRESPONSE']._serialized_start = 864
    _globals['_MSGBEGINUNLOCKINGRESPONSE']._serialized_end = 933
    _globals['_MSGEXTENDLOCKUP']._serialized_start = 936
    _globals['_MSGEXTENDLOCKUP']._serialized_end = 1129
    _globals['_MSGEXTENDLOCKUPRESPONSE']._serialized_start = 1131
    _globals['_MSGEXTENDLOCKUPRESPONSE']._serialized_end = 1173
    _globals['_MSGFORCEUNLOCK']._serialized_start = 1176
    _globals['_MSGFORCEUNLOCK']._serialized_end = 1370
    _globals['_MSGFORCEUNLOCKRESPONSE']._serialized_start = 1372
    _globals['_MSGFORCEUNLOCKRESPONSE']._serialized_end = 1413
    _globals['_MSGSETREWARDRECEIVERADDRESS']._serialized_start = 1416
    _globals['_MSGSETREWARDRECEIVERADDRESS']._serialized_end = 1596
    _globals['_MSGSETREWARDRECEIVERADDRESSRESPONSE']._serialized_start = 1598
    _globals['_MSGSETREWARDRECEIVERADDRESSRESPONSE']._serialized_end = 1652
    _globals['_MSG']._serialized_start = 1655
    _globals['_MSG']._serialized_end = 2248