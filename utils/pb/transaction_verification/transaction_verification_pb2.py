# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: transaction_verification.proto
# Protobuf Python Version: 4.25.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1etransaction_verification.proto\x12\x05hello\"\x1d\n\rVerifyRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"\"\n\x0eVerifyResponse\x12\x10\n\x08\x64\x65\x63ision\x18\x01 \x01(\x08\x32\x45\n\x0cVerifService\x12\x35\n\x06Verify\x12\x14.hello.VerifyRequest\x1a\x15.hello.VerifyResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'transaction_verification_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_VERIFYREQUEST']._serialized_start=41
  _globals['_VERIFYREQUEST']._serialized_end=70
  _globals['_VERIFYRESPONSE']._serialized_start=72
  _globals['_VERIFYRESPONSE']._serialized_end=106
  _globals['_VERIFSERVICE']._serialized_start=108
  _globals['_VERIFSERVICE']._serialized_end=177
# @@protoc_insertion_point(module_scope)
