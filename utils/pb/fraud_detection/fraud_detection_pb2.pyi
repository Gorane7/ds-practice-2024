from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Empty_fraud(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class VectorClockInp_fraud(_message.Message):
    __slots__ = ("vector_clock",)
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    vector_clock: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, vector_clock: _Optional[_Iterable[int]] = ...) -> None: ...

class HelloRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class HelloResponse(_message.Message):
    __slots__ = ("greeting",)
    GREETING_FIELD_NUMBER: _ClassVar[int]
    greeting: str
    def __init__(self, greeting: _Optional[str] = ...) -> None: ...

class FraudRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class FraudResponse(_message.Message):
    __slots__ = ("decision",)
    DECISION_FIELD_NUMBER: _ClassVar[int]
    decision: bool
    def __init__(self, decision: bool = ...) -> None: ...
