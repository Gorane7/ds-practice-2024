# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: fraud_detection.proto
# Protobuf Python Version: 4.25.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x66raud_detection.proto\x12\x05hello\"\r\n\x0b\x45mpty_fraud\",\n\x14VectorClockInp_fraud\x12\x14\n\x0cvector_clock\x18\x01 \x03(\x05\"\x1c\n\x0cHelloRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"!\n\rHelloResponse\x12\x10\n\x08greeting\x18\x01 \x01(\t\"\x1c\n\x0c\x46raudRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"!\n\rFraudResponse\x12\x10\n\x08\x64\x65\x63ision\x18\x01 \x01(\x08\x32\xc5\x01\n\x0cHelloService\x12\x35\n\x08SayHello\x12\x13.hello.HelloRequest\x1a\x14.hello.HelloResponse\x12\x38\n\x0b\x44\x65tectFraud\x12\x13.hello.FraudRequest\x1a\x14.hello.FraudResponse\x12\x44\n\x11VectorClockUpdate\x12\x1b.hello.VectorClockInp_fraud\x1a\x12.hello.Empty_fraudb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'fraud_detection_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_EMPTY_FRAUD']._serialized_start=32
  _globals['_EMPTY_FRAUD']._serialized_end=45
  _globals['_VECTORCLOCKINP_FRAUD']._serialized_start=47
  _globals['_VECTORCLOCKINP_FRAUD']._serialized_end=91
  _globals['_HELLOREQUEST']._serialized_start=93
  _globals['_HELLOREQUEST']._serialized_end=121
  _globals['_HELLORESPONSE']._serialized_start=123
  _globals['_HELLORESPONSE']._serialized_end=156
  _globals['_FRAUDREQUEST']._serialized_start=158
  _globals['_FRAUDREQUEST']._serialized_end=186
  _globals['_FRAUDRESPONSE']._serialized_start=188
  _globals['_FRAUDRESPONSE']._serialized_end=221
  _globals['_HELLOSERVICE']._serialized_start=224
  _globals['_HELLOSERVICE']._serialized_end=421
# @@protoc_insertion_point(module_scope)
