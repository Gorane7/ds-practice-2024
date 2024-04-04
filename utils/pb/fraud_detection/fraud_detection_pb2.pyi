from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class KillOrder_fraud(_message.Message):
    __slots__ = ("order_id",)
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    order_id: int
    def __init__(self, order_id: _Optional[int] = ...) -> None: ...

class Empty_fraud(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class VectorClockInp_fraud(_message.Message):
    __slots__ = ("vector_clock", "order_id")
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    vector_clock: _containers.RepeatedScalarFieldContainer[int]
    order_id: int
    def __init__(self, vector_clock: _Optional[_Iterable[int]] = ..., order_id: _Optional[int] = ...) -> None: ...

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

class CreditInfo2(_message.Message):
    __slots__ = ("number", "expirationDate", "cvv")
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    EXPIRATIONDATE_FIELD_NUMBER: _ClassVar[int]
    CVV_FIELD_NUMBER: _ClassVar[int]
    number: str
    expirationDate: str
    cvv: str
    def __init__(self, number: _Optional[str] = ..., expirationDate: _Optional[str] = ..., cvv: _Optional[str] = ...) -> None: ...

class FraudRequest(_message.Message):
    __slots__ = ("name", "creditInfo", "order_id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREDITINFO_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    creditInfo: CreditInfo2
    order_id: int
    def __init__(self, name: _Optional[str] = ..., creditInfo: _Optional[_Union[CreditInfo2, _Mapping]] = ..., order_id: _Optional[int] = ...) -> None: ...

class FraudResponse(_message.Message):
    __slots__ = ("decision",)
    DECISION_FIELD_NUMBER: _ClassVar[int]
    decision: bool
    def __init__(self, decision: bool = ...) -> None: ...
