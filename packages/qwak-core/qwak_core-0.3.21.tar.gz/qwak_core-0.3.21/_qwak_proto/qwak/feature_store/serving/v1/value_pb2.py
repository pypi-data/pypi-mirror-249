# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: qwak/feature_store/serving/v1/value.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n)qwak/feature_store/serving/v1/value.proto\x12$com.qwak.ai.feature.store.serving.v1\x1a\x1fgoogle/protobuf/timestamp.proto\"\xad\x02\n\x07ValueV1\x12\x0e\n\x06is_set\x18\x01 \x01(\x08\x12\x13\n\tbytes_val\x18\x02 \x01(\x0cH\x00\x12\x14\n\nstring_val\x18\x03 \x01(\tH\x00\x12\x13\n\tint32_val\x18\x04 \x01(\x05H\x00\x12\x13\n\tint64_val\x18\x05 \x01(\x03H\x00\x12\x14\n\ndouble_val\x18\x06 \x01(\x01H\x00\x12\x13\n\tfloat_val\x18\x07 \x01(\x02H\x00\x12\x12\n\x08\x62ool_val\x18\x08 \x01(\x08H\x00\x12\x33\n\rtimestamp_val\x18\t \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x00\x12\x42\n\tarray_val\x18\n \x01(\x0b\x32-.com.qwak.ai.feature.store.serving.v1.ArrayV1H\x00\x42\x05\n\x03val\"K\n\x07\x41rrayV1\x12@\n\tarray_val\x18\x01 \x03(\x0b\x32-.com.qwak.ai.feature.store.serving.v1.ValueV1B&\n$com.qwak.ai.feature.store.serving.v1b\x06proto3')



_VALUEV1 = DESCRIPTOR.message_types_by_name['ValueV1']
_ARRAYV1 = DESCRIPTOR.message_types_by_name['ArrayV1']
ValueV1 = _reflection.GeneratedProtocolMessageType('ValueV1', (_message.Message,), {
  'DESCRIPTOR' : _VALUEV1,
  '__module__' : 'qwak.feature_store.serving.v1.value_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.ai.feature.store.serving.v1.ValueV1)
  })
_sym_db.RegisterMessage(ValueV1)

ArrayV1 = _reflection.GeneratedProtocolMessageType('ArrayV1', (_message.Message,), {
  'DESCRIPTOR' : _ARRAYV1,
  '__module__' : 'qwak.feature_store.serving.v1.value_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.ai.feature.store.serving.v1.ArrayV1)
  })
_sym_db.RegisterMessage(ArrayV1)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n$com.qwak.ai.feature.store.serving.v1'
  _VALUEV1._serialized_start=117
  _VALUEV1._serialized_end=418
  _ARRAYV1._serialized_start=420
  _ARRAYV1._serialized_end=495
# @@protoc_insertion_point(module_scope)
