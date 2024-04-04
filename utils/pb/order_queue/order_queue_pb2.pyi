from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class EnqueueRequest(_message.Message):
    __slots__ = ("booknames", "priority")
    BOOKNAMES_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    booknames: _containers.RepeatedScalarFieldContainer[str]
    priority: int
    def __init__(self, booknames: _Optional[_Iterable[str]] = ..., priority: _Optional[int] = ...) -> None: ...

class EnqueueResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class DequeueRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DequeueResponse(_message.Message):
    __slots__ = ("booknames", "have_order")
    BOOKNAMES_FIELD_NUMBER: _ClassVar[int]
    HAVE_ORDER_FIELD_NUMBER: _ClassVar[int]
    booknames: _containers.RepeatedScalarFieldContainer[str]
    have_order: bool
    def __init__(self, booknames: _Optional[_Iterable[str]] = ..., have_order: bool = ...) -> None: ...
