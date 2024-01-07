"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from .....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n,cosmos/base/snapshots/v1beta1/snapshot.proto\x12\x1dcosmos.base.snapshots.v1beta1\x1a\x14gogoproto/gogo.proto"\x89\x01\n\x08Snapshot\x12\x0e\n\x06height\x18\x01 \x01(\x04\x12\x0e\n\x06format\x18\x02 \x01(\r\x12\x0e\n\x06chunks\x18\x03 \x01(\r\x12\x0c\n\x04hash\x18\x04 \x01(\x0c\x12?\n\x08metadata\x18\x05 \x01(\x0b2\'.cosmos.base.snapshots.v1beta1.MetadataB\x04\xc8\xde\x1f\x00" \n\x08Metadata\x12\x14\n\x0cchunk_hashes\x18\x01 \x03(\x0c"\xd1\x03\n\x0cSnapshotItem\x12A\n\x05store\x18\x01 \x01(\x0b20.cosmos.base.snapshots.v1beta1.SnapshotStoreItemH\x00\x12I\n\x04iavl\x18\x02 \x01(\x0b2/.cosmos.base.snapshots.v1beta1.SnapshotIAVLItemB\x08\xe2\xde\x1f\x04IAVLH\x00\x12I\n\textension\x18\x03 \x01(\x0b24.cosmos.base.snapshots.v1beta1.SnapshotExtensionMetaH\x00\x12T\n\x11extension_payload\x18\x04 \x01(\x0b27.cosmos.base.snapshots.v1beta1.SnapshotExtensionPayloadH\x00\x12E\n\x02kv\x18\x05 \x01(\x0b2-.cosmos.base.snapshots.v1beta1.SnapshotKVItemB\x08\x18\x01\xe2\xde\x1f\x02KVH\x00\x12C\n\x06schema\x18\x06 \x01(\x0b2-.cosmos.base.snapshots.v1beta1.SnapshotSchemaB\x02\x18\x01H\x00B\x06\n\x04item"!\n\x11SnapshotStoreItem\x12\x0c\n\x04name\x18\x01 \x01(\t"O\n\x10SnapshotIAVLItem\x12\x0b\n\x03key\x18\x01 \x01(\x0c\x12\r\n\x05value\x18\x02 \x01(\x0c\x12\x0f\n\x07version\x18\x03 \x01(\x03\x12\x0e\n\x06height\x18\x04 \x01(\x05"5\n\x15SnapshotExtensionMeta\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0e\n\x06format\x18\x02 \x01(\r"+\n\x18SnapshotExtensionPayload\x12\x0f\n\x07payload\x18\x01 \x01(\x0c"0\n\x0eSnapshotKVItem\x12\x0b\n\x03key\x18\x01 \x01(\x0c\x12\r\n\x05value\x18\x02 \x01(\x0c:\x02\x18\x01""\n\x0eSnapshotSchema\x12\x0c\n\x04keys\x18\x01 \x03(\x0c:\x02\x18\x01B.Z,github.com/cosmos/cosmos-sdk/snapshots/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.base.snapshots.v1beta1.snapshot_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z,github.com/cosmos/cosmos-sdk/snapshots/types'
    _SNAPSHOT.fields_by_name['metadata']._options = None
    _SNAPSHOT.fields_by_name['metadata']._serialized_options = b'\xc8\xde\x1f\x00'
    _SNAPSHOTITEM.fields_by_name['iavl']._options = None
    _SNAPSHOTITEM.fields_by_name['iavl']._serialized_options = b'\xe2\xde\x1f\x04IAVL'
    _SNAPSHOTITEM.fields_by_name['kv']._options = None
    _SNAPSHOTITEM.fields_by_name['kv']._serialized_options = b'\x18\x01\xe2\xde\x1f\x02KV'
    _SNAPSHOTITEM.fields_by_name['schema']._options = None
    _SNAPSHOTITEM.fields_by_name['schema']._serialized_options = b'\x18\x01'
    _SNAPSHOTKVITEM._options = None
    _SNAPSHOTKVITEM._serialized_options = b'\x18\x01'
    _SNAPSHOTSCHEMA._options = None
    _SNAPSHOTSCHEMA._serialized_options = b'\x18\x01'
    _globals['_SNAPSHOT']._serialized_start = 102
    _globals['_SNAPSHOT']._serialized_end = 239
    _globals['_METADATA']._serialized_start = 241
    _globals['_METADATA']._serialized_end = 273
    _globals['_SNAPSHOTITEM']._serialized_start = 276
    _globals['_SNAPSHOTITEM']._serialized_end = 741
    _globals['_SNAPSHOTSTOREITEM']._serialized_start = 743
    _globals['_SNAPSHOTSTOREITEM']._serialized_end = 776
    _globals['_SNAPSHOTIAVLITEM']._serialized_start = 778
    _globals['_SNAPSHOTIAVLITEM']._serialized_end = 857
    _globals['_SNAPSHOTEXTENSIONMETA']._serialized_start = 859
    _globals['_SNAPSHOTEXTENSIONMETA']._serialized_end = 912
    _globals['_SNAPSHOTEXTENSIONPAYLOAD']._serialized_start = 914
    _globals['_SNAPSHOTEXTENSIONPAYLOAD']._serialized_end = 957
    _globals['_SNAPSHOTKVITEM']._serialized_start = 959
    _globals['_SNAPSHOTKVITEM']._serialized_end = 1007
    _globals['_SNAPSHOTSCHEMA']._serialized_start = 1009
    _globals['_SNAPSHOTSCHEMA']._serialized_end = 1043