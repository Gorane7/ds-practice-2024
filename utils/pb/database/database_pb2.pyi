from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OverwriteDBRequest(_message.Message):
    __slots__ = ("fields",)
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    fields: _containers.RepeatedCompositeFieldContainer[Field]
    def __init__(self, fields: _Optional[_Iterable[_Union[Field, _Mapping]]] = ...) -> None: ...

class Field(_message.Message):
    __slots__ = ("book_name", "amount")
    BOOK_NAME_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    book_name: str
    amount: int
    def __init__(self, book_name: _Optional[str] = ..., amount: _Optional[int] = ...) -> None: ...

class OverwriteDBResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

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
    __slots__ = ("field", "value", "fresh", "modify_id")
    FIELD_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    FRESH_FIELD_NUMBER: _ClassVar[int]
    MODIFY_ID_FIELD_NUMBER: _ClassVar[int]
    field: str
    value: int
    fresh: bool
    modify_id: int
    def __init__(self, field: _Optional[str] = ..., value: _Optional[int] = ..., fresh: bool = ..., modify_id: _Optional[int] = ...) -> None: ...

class ModifyResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class ModifyCommitRequest(_message.Message):
    __slots__ = ("modify_id", "to_commit", "fresh")
    MODIFY_ID_FIELD_NUMBER: _ClassVar[int]
    TO_COMMIT_FIELD_NUMBER: _ClassVar[int]
    FRESH_FIELD_NUMBER: _ClassVar[int]
    modify_id: int
    to_commit: bool
    fresh: bool
    def __init__(self, modify_id: _Optional[int] = ..., to_commit: bool = ..., fresh: bool = ...) -> None: ...

class ModifyCommitResponse(_message.Message):
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
