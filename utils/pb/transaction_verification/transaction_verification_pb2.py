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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1etransaction_verification.proto\x12\x05hello\"\r\n\x0b\x45mpty_trans\",\n\x14VectorClockInp_trans\x12\x14\n\x0cvector_clock\x18\x01 \x03(\x05\"&\n\x04Item\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08quantity\x18\x02 \x01(\x05\")\n\x08UserInfo\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontact\x18\x02 \x01(\t\"A\n\nCreditInfo\x12\x0e\n\x06number\x18\x01 \x01(\t\x12\x16\n\x0e\x65xpirationDate\x18\x02 \x01(\t\x12\x0b\n\x03\x63vv\x18\x03 \x01(\t\"u\n\rVerifyRequest\x12\x1a\n\x05items\x18\x01 \x03(\x0b\x32\x0b.hello.Item\x12!\n\x08userInfo\x18\x02 \x01(\x0b\x32\x0f.hello.UserInfo\x12%\n\ncreditInfo\x18\x03 \x01(\x0b\x32\x11.hello.CreditInfo\"\"\n\x0eVerifyResponse\x12\x10\n\x08\x64\x65\x63ision\x18\x01 \x01(\x05\x32\x8b\x01\n\x0cVerifService\x12\x35\n\x06Verify\x12\x14.hello.VerifyRequest\x1a\x15.hello.VerifyResponse\x12\x44\n\x11VectorClockUpdate\x12\x1b.hello.VectorClockInp_trans\x1a\x12.hello.Empty_transb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'transaction_verification_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_EMPTY_TRANS']._serialized_start=41
  _globals['_EMPTY_TRANS']._serialized_end=54
  _globals['_VECTORCLOCKINP_TRANS']._serialized_start=56
  _globals['_VECTORCLOCKINP_TRANS']._serialized_end=100
  _globals['_ITEM']._serialized_start=102
  _globals['_ITEM']._serialized_end=140
  _globals['_USERINFO']._serialized_start=142
  _globals['_USERINFO']._serialized_end=183
  _globals['_CREDITINFO']._serialized_start=185
  _globals['_CREDITINFO']._serialized_end=250
  _globals['_VERIFYREQUEST']._serialized_start=252
  _globals['_VERIFYREQUEST']._serialized_end=369
  _globals['_VERIFYRESPONSE']._serialized_start=371
  _globals['_VERIFYRESPONSE']._serialized_end=405
  _globals['_VERIFSERVICE']._serialized_start=408
  _globals['_VERIFSERVICE']._serialized_end=547
# @@protoc_insertion_point(module_scope)
