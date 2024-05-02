from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PaymentRequest(_message.Message):
    __slots__ = ("payment_id", "amount", "credit_card")
    PAYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    CREDIT_CARD_FIELD_NUMBER: _ClassVar[int]
    payment_id: int
    amount: int
    credit_card: int
    def __init__(self, payment_id: _Optional[int] = ..., amount: _Optional[int] = ..., credit_card: _Optional[int] = ...) -> None: ...

class PaymentResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class PaymentConfirmation(_message.Message):
    __slots__ = ("payment_id", "perform_payment")
    PAYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    PERFORM_PAYMENT_FIELD_NUMBER: _ClassVar[int]
    payment_id: int
    perform_payment: bool
    def __init__(self, payment_id: _Optional[int] = ..., perform_payment: bool = ...) -> None: ...
