# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: order_queue.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11order_queue.proto\x12\x05hello\"#\n\x0e\x45nqueueRequest\x12\x11\n\tbooknames\x18\x01 \x03(\t\"\"\n\x0f\x45nqueueResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x10\n\x0e\x44\x65queueRequest\"8\n\x0f\x44\x65queueResponse\x12\x11\n\tbooknames\x18\x01 \x03(\t\x12\x12\n\nhave_order\x18\x02 \x01(\x08\x32\x80\x01\n\nOrderQueue\x12\x38\n\x07\x45nqueue\x12\x15.hello.EnqueueRequest\x1a\x16.hello.EnqueueResponse\x12\x38\n\x07\x44\x65queue\x12\x15.hello.DequeueRequest\x1a\x16.hello.DequeueResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'order_queue_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_ENQUEUEREQUEST']._serialized_start=28
  _globals['_ENQUEUEREQUEST']._serialized_end=63
  _globals['_ENQUEUERESPONSE']._serialized_start=65
  _globals['_ENQUEUERESPONSE']._serialized_end=99
  _globals['_DEQUEUEREQUEST']._serialized_start=101
  _globals['_DEQUEUEREQUEST']._serialized_end=117
  _globals['_DEQUEUERESPONSE']._serialized_start=119
  _globals['_DEQUEUERESPONSE']._serialized_end=175
  _globals['_ORDERQUEUE']._serialized_start=178
  _globals['_ORDERQUEUE']._serialized_end=306
# @@protoc_insertion_point(module_scope)