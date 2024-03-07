from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Item(_message.Message):
    __slots__ = ("name", "quantity")
    NAME_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    name: str
    quantity: int
    def __init__(self, name: _Optional[str] = ..., quantity: _Optional[int] = ...) -> None: ...

class UserInfo(_message.Message):
    __slots__ = ("name", "contact")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONTACT_FIELD_NUMBER: _ClassVar[int]
    name: str
    contact: str
    def __init__(self, name: _Optional[str] = ..., contact: _Optional[str] = ...) -> None: ...

class CreditInfo(_message.Message):
    __slots__ = ("number", "expirationDate", "cvv")
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    EXPIRATIONDATE_FIELD_NUMBER: _ClassVar[int]
    CVV_FIELD_NUMBER: _ClassVar[int]
    number: str
    expirationDate: str
    cvv: str
    def __init__(self, number: _Optional[str] = ..., expirationDate: _Optional[str] = ..., cvv: _Optional[str] = ...) -> None: ...

class VerifyRequest(_message.Message):
    __slots__ = ("items", "userInfo", "creditInfo")
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    USERINFO_FIELD_NUMBER: _ClassVar[int]
    CREDITINFO_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[Item]
    userInfo: UserInfo
    creditInfo: CreditInfo
    def __init__(self, items: _Optional[_Iterable[_Union[Item, _Mapping]]] = ..., userInfo: _Optional[_Union[UserInfo, _Mapping]] = ..., creditInfo: _Optional[_Union[CreditInfo, _Mapping]] = ...) -> None: ...

class VerifyResponse(_message.Message):
    __slots__ = ("decision",)
    DECISION_FIELD_NUMBER: _ClassVar[int]
    decision: int
    def __init__(self, decision: _Optional[int] = ...) -> None: ...
