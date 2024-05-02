from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ReadRequest(_message.Message):
    __slots__ = ("field",)
    FIELD_FIELD_NUMBER: _ClassVar[int]
    field: str
    def __init__(self, field: _Optional[str] = ...) -> None: ...

class ReadResponse(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: int
    def __init__(self, value: _Optional[int] = ...) -> None: ...

class WriteRequest(_message.Message):
    __slots__ = ("field", "value", "fresh")
    FIELD_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    FRESH_FIELD_NUMBER: _ClassVar[int]
    field: str
    value: int
    fresh: bool
    def __init__(self, field: _Optional[str] = ..., value: _Optional[int] = ..., fresh: bool = ...) -> None: ...

class WriteResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ModifyRequest(_message.Message):
    __slots__ = ("fied", "value", "fresh")
    FIED_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    FRESH_FIELD_NUMBER: _ClassVar[int]
    fied: str
    value: int
    fresh: bool
    def __init__(self, fied: _Optional[str] = ..., value: _Optional[int] = ..., fresh: bool = ...) -> None: ...

class ModifyResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LockRequest(_message.Message):
    __slots__ = ("field", "lock_id")
    FIELD_FIELD_NUMBER: _ClassVar[int]
    LOCK_ID_FIELD_NUMBER: _ClassVar[int]
    field: str
    lock_id: int
    def __init__(self, field: _Optional[str] = ..., lock_id: _Optional[int] = ...) -> None: ...

class LockResponse(_message.Message):
    __slots__ = ("ok", "other_id")
    OK_FIELD_NUMBER: _ClassVar[int]
    OTHER_ID_FIELD_NUMBER: _ClassVar[int]
    ok: bool
    other_id: int
    def __init__(self, ok: bool = ..., other_id: _Optional[int] = ...) -> None: ...

class ReleaseRequest(_message.Message):
    __slots__ = ("field", "lock_id")
    FIELD_FIELD_NUMBER: _ClassVar[int]
    LOCK_ID_FIELD_NUMBER: _ClassVar[int]
    field: str
    lock_id: int
    def __init__(self, field: _Optional[str] = ..., lock_id: _Optional[int] = ...) -> None: ...

class ReleaseResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
