from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class KillOrder_sugg(_message.Message):
    __slots__ = ("order_id",)
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    order_id: int
    def __init__(self, order_id: _Optional[int] = ...) -> None: ...

class Empty_sugg(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class VectorClockInp_sugg(_message.Message):
    __slots__ = ("vector_clock", "order_id")
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    vector_clock: _containers.RepeatedScalarFieldContainer[int]
    order_id: int
    def __init__(self, vector_clock: _Optional[_Iterable[int]] = ..., order_id: _Optional[int] = ...) -> None: ...

class Book(_message.Message):
    __slots__ = ("bookId", "title", "author")
    BOOKID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    bookId: str
    title: str
    author: str
    def __init__(self, bookId: _Optional[str] = ..., title: _Optional[str] = ..., author: _Optional[str] = ...) -> None: ...

class SuggestionRequest(_message.Message):
    __slots__ = ("books", "ordered", "order_id")
    BOOKS_FIELD_NUMBER: _ClassVar[int]
    ORDERED_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    books: _containers.RepeatedCompositeFieldContainer[Book]
    ordered: _containers.RepeatedScalarFieldContainer[str]
    order_id: int
    def __init__(self, books: _Optional[_Iterable[_Union[Book, _Mapping]]] = ..., ordered: _Optional[_Iterable[str]] = ..., order_id: _Optional[int] = ...) -> None: ...

class SuggestionResponse(_message.Message):
    __slots__ = ("books",)
    BOOKS_FIELD_NUMBER: _ClassVar[int]
    books: _containers.RepeatedCompositeFieldContainer[Book]
    def __init__(self, books: _Optional[_Iterable[_Union[Book, _Mapping]]] = ...) -> None: ...
