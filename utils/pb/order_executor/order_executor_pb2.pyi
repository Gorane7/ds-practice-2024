from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TokenRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TokenResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RestartRequest(_message.Message):
    __slots__ = ("restarter_id",)
    RESTARTER_ID_FIELD_NUMBER: _ClassVar[int]
    restarter_id: int
    def __init__(self, restarter_id: _Optional[int] = ...) -> None: ...

class RestartResponse(_message.Message):
    __slots__ = ("next_id", "restart_success")
    NEXT_ID_FIELD_NUMBER: _ClassVar[int]
    RESTART_SUCCESS_FIELD_NUMBER: _ClassVar[int]
    next_id: int
    restart_success: bool
    def __init__(self, next_id: _Optional[int] = ..., restart_success: bool = ...) -> None: ...
