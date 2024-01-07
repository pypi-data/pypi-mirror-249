"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ...gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from ...cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19osmosis/lockup/lock.proto\x12\x0eosmosis.lockup\x1a\x14gogoproto/gogo.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1ecosmos/base/v1beta1/coin.proto"\x85\x03\n\nPeriodLock\x12\n\n\x02ID\x18\x01 \x01(\x04\x12\x1f\n\x05owner\x18\x02 \x01(\tB\x10\xf2\xde\x1f\x0cyaml:"owner"\x12^\n\x08duration\x18\x03 \x01(\x0b2\x19.google.protobuf.DurationB1\xc8\xde\x1f\x00\xea\xde\x1f\x12duration,omitempty\xf2\xde\x1f\x0fyaml:"duration"\x98\xdf\x1f\x01\x12I\n\x08end_time\x18\x04 \x01(\x0b2\x1a.google.protobuf.TimestampB\x1b\xc8\xde\x1f\x00\xf2\xde\x1f\x0fyaml:"end_time"\x90\xdf\x1f\x01\x12Z\n\x05coins\x18\x05 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x12C\n\x17reward_receiver_address\x18\x06 \x01(\tB"\xf2\xde\x1f\x1eyaml:"reward_receiver_address""\xee\x01\n\x0eQueryCondition\x126\n\x0flock_query_type\x18\x01 \x01(\x0e2\x1d.osmosis.lockup.LockQueryType\x12\r\n\x05denom\x18\x02 \x01(\t\x12H\n\x08duration\x18\x03 \x01(\x0b2\x19.google.protobuf.DurationB\x1b\xc8\xde\x1f\x00\xf2\xde\x1f\x0fyaml:"duration"\x98\xdf\x1f\x01\x12K\n\ttimestamp\x18\x04 \x01(\x0b2\x1a.google.protobuf.TimestampB\x1c\xc8\xde\x1f\x00\xf2\xde\x1f\x10yaml:"timestamp"\x90\xdf\x1f\x01"\xeb\x01\n\rSyntheticLock\x12\x1a\n\x12underlying_lock_id\x18\x01 \x01(\x04\x12\x13\n\x0bsynth_denom\x18\x02 \x01(\t\x12I\n\x08end_time\x18\x03 \x01(\x0b2\x1a.google.protobuf.TimestampB\x1b\xc8\xde\x1f\x00\xf2\xde\x1f\x0fyaml:"end_time"\x90\xdf\x1f\x01\x12^\n\x08duration\x18\x04 \x01(\x0b2\x19.google.protobuf.DurationB1\xc8\xde\x1f\x00\xea\xde\x1f\x12duration,omitempty\xf2\xde\x1f\x0fyaml:"duration"\x98\xdf\x1f\x01*J\n\rLockQueryType\x12\x0e\n\nByDuration\x10\x00\x12\n\n\x06ByTime\x10\x01\x12\n\n\x06NoLock\x10\x02\x12\x0b\n\x07ByGroup\x10\x03\x1a\x04\x88\xa3\x1e\x00B4Z2github.com/osmosis-labs/osmosis/v21/x/lockup/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.lockup.lock_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z2github.com/osmosis-labs/osmosis/v21/x/lockup/types'
    _LOCKQUERYTYPE._options = None
    _LOCKQUERYTYPE._serialized_options = b'\x88\xa3\x1e\x00'
    _PERIODLOCK.fields_by_name['owner']._options = None
    _PERIODLOCK.fields_by_name['owner']._serialized_options = b'\xf2\xde\x1f\x0cyaml:"owner"'
    _PERIODLOCK.fields_by_name['duration']._options = None
    _PERIODLOCK.fields_by_name['duration']._serialized_options = b'\xc8\xde\x1f\x00\xea\xde\x1f\x12duration,omitempty\xf2\xde\x1f\x0fyaml:"duration"\x98\xdf\x1f\x01'
    _PERIODLOCK.fields_by_name['end_time']._options = None
    _PERIODLOCK.fields_by_name['end_time']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x0fyaml:"end_time"\x90\xdf\x1f\x01'
    _PERIODLOCK.fields_by_name['coins']._options = None
    _PERIODLOCK.fields_by_name['coins']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _PERIODLOCK.fields_by_name['reward_receiver_address']._options = None
    _PERIODLOCK.fields_by_name['reward_receiver_address']._serialized_options = b'\xf2\xde\x1f\x1eyaml:"reward_receiver_address"'
    _QUERYCONDITION.fields_by_name['duration']._options = None
    _QUERYCONDITION.fields_by_name['duration']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x0fyaml:"duration"\x98\xdf\x1f\x01'
    _QUERYCONDITION.fields_by_name['timestamp']._options = None
    _QUERYCONDITION.fields_by_name['timestamp']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x10yaml:"timestamp"\x90\xdf\x1f\x01'
    _SYNTHETICLOCK.fields_by_name['end_time']._options = None
    _SYNTHETICLOCK.fields_by_name['end_time']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x0fyaml:"end_time"\x90\xdf\x1f\x01'
    _SYNTHETICLOCK.fields_by_name['duration']._options = None
    _SYNTHETICLOCK.fields_by_name['duration']._serialized_options = b'\xc8\xde\x1f\x00\xea\xde\x1f\x12duration,omitempty\xf2\xde\x1f\x0fyaml:"duration"\x98\xdf\x1f\x01'
    _globals['_LOCKQUERYTYPE']._serialized_start = 1035
    _globals['_LOCKQUERYTYPE']._serialized_end = 1109
    _globals['_PERIODLOCK']._serialized_start = 165
    _globals['_PERIODLOCK']._serialized_end = 554
    _globals['_QUERYCONDITION']._serialized_start = 557
    _globals['_QUERYCONDITION']._serialized_end = 795
    _globals['_SYNTHETICLOCK']._serialized_start = 798
    _globals['_SYNTHETICLOCK']._serialized_end = 1033