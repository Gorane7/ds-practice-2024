# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: database.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0e\x64\x61tabase.proto\x12\x05hello\"\x1c\n\x0bReadRequest\x12\r\n\x05\x66ield\x18\x01 \x01(\t\"\x1d\n\x0cReadResponse\x12\r\n\x05value\x18\x01 \x01(\x05\";\n\x0cWriteRequest\x12\r\n\x05\x66ield\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05\x12\r\n\x05\x66resh\x18\x03 \x01(\x08\"\x0f\n\rWriteResponse\"O\n\rModifyRequest\x12\r\n\x05\x66ield\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05\x12\r\n\x05\x66resh\x18\x03 \x01(\x08\x12\x11\n\tmodify_id\x18\x04 \x01(\x03\"!\n\x0eModifyResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"J\n\x13ModifyCommitRequest\x12\x11\n\tmodify_id\x18\x01 \x01(\x03\x12\x11\n\tto_commit\x18\x02 \x01(\x08\x12\r\n\x05\x66resh\x18\x03 \x01(\x08\"\x16\n\x14ModifyCommitResponse\"-\n\x0bLockRequest\x12\r\n\x05\x66ield\x18\x01 \x01(\t\x12\x0f\n\x07lock_id\x18\x02 \x01(\x03\",\n\x0cLockResponse\x12\n\n\x02ok\x18\x01 \x01(\x08\x12\x10\n\x08other_id\x18\x02 \x01(\x03\"0\n\x0eReleaseRequest\x12\r\n\x05\x66ield\x18\x01 \x01(\t\x12\x0f\n\x07lock_id\x18\x02 \x01(\x03\"\x11\n\x0fReleaseResponse2\xda\x02\n\x08\x44\x61tabase\x12/\n\x04Read\x12\x12.hello.ReadRequest\x1a\x13.hello.ReadResponse\x12\x32\n\x05Write\x12\x13.hello.WriteRequest\x1a\x14.hello.WriteResponse\x12\x35\n\x06Modify\x12\x14.hello.ModifyRequest\x1a\x15.hello.ModifyResponse\x12G\n\x0cModifyCommit\x12\x1a.hello.ModifyCommitRequest\x1a\x1b.hello.ModifyCommitResponse\x12/\n\x04Lock\x12\x12.hello.LockRequest\x1a\x13.hello.LockResponse\x12\x38\n\x07Release\x12\x15.hello.ReleaseRequest\x1a\x16.hello.ReleaseResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'database_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_READREQUEST']._serialized_start=25
  _globals['_READREQUEST']._serialized_end=53
  _globals['_READRESPONSE']._serialized_start=55
  _globals['_READRESPONSE']._serialized_end=84
  _globals['_WRITEREQUEST']._serialized_start=86
  _globals['_WRITEREQUEST']._serialized_end=145
  _globals['_WRITERESPONSE']._serialized_start=147
  _globals['_WRITERESPONSE']._serialized_end=162
  _globals['_MODIFYREQUEST']._serialized_start=164
  _globals['_MODIFYREQUEST']._serialized_end=243
  _globals['_MODIFYRESPONSE']._serialized_start=245
  _globals['_MODIFYRESPONSE']._serialized_end=278
  _globals['_MODIFYCOMMITREQUEST']._serialized_start=280
  _globals['_MODIFYCOMMITREQUEST']._serialized_end=354
  _globals['_MODIFYCOMMITRESPONSE']._serialized_start=356
  _globals['_MODIFYCOMMITRESPONSE']._serialized_end=378
  _globals['_LOCKREQUEST']._serialized_start=380
  _globals['_LOCKREQUEST']._serialized_end=425
  _globals['_LOCKRESPONSE']._serialized_start=427
  _globals['_LOCKRESPONSE']._serialized_end=471
  _globals['_RELEASEREQUEST']._serialized_start=473
  _globals['_RELEASEREQUEST']._serialized_end=521
  _globals['_RELEASERESPONSE']._serialized_start=523
  _globals['_RELEASERESPONSE']._serialized_end=540
  _globals['_DATABASE']._serialized_start=543
  _globals['_DATABASE']._serialized_end=889
# @@protoc_insertion_point(module_scope)
