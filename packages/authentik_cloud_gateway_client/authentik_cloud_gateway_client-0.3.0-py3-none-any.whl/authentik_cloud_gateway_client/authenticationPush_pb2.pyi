from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class AuthenticationResponseStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN: _ClassVar[AuthenticationResponseStatus]
    SENT: _ClassVar[AuthenticationResponseStatus]
    FAILED: _ClassVar[AuthenticationResponseStatus]
    ANSWERED: _ClassVar[AuthenticationResponseStatus]

UNKNOWN: AuthenticationResponseStatus
SENT: AuthenticationResponseStatus
FAILED: AuthenticationResponseStatus
ANSWERED: AuthenticationResponseStatus

class AuthenticationRequest(_message.Message):
    __slots__ = ("device_uuid", "device_token", "tx_id", "mode", "items", "attributes")

    class Attributes(_message.Message):
        __slots__ = ("title", "body", "client_ip", "geo", "extra")

        class Geo(_message.Message):
            __slots__ = ("lat", "long")
            LAT_FIELD_NUMBER: _ClassVar[int]
            LONG_FIELD_NUMBER: _ClassVar[int]
            lat: float
            long: float
            def __init__(self, lat: _Optional[float] = ..., long: _Optional[float] = ...) -> None: ...

        class ExtraEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: str
            def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
        TITLE_FIELD_NUMBER: _ClassVar[int]
        BODY_FIELD_NUMBER: _ClassVar[int]
        CLIENT_IP_FIELD_NUMBER: _ClassVar[int]
        GEO_FIELD_NUMBER: _ClassVar[int]
        EXTRA_FIELD_NUMBER: _ClassVar[int]
        title: str
        body: str
        client_ip: str
        geo: AuthenticationRequest.Attributes.Geo
        extra: _containers.ScalarMap[str, str]
        def __init__(
            self,
            title: _Optional[str] = ...,
            body: _Optional[str] = ...,
            client_ip: _Optional[str] = ...,
            geo: _Optional[_Union[AuthenticationRequest.Attributes.Geo, _Mapping]] = ...,
            extra: _Optional[_Mapping[str, str]] = ...,
        ) -> None: ...
    DEVICE_UUID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TX_ID_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    device_uuid: str
    device_token: str
    tx_id: str
    mode: str
    items: _containers.RepeatedScalarFieldContainer[str]
    attributes: AuthenticationRequest.Attributes
    def __init__(
        self,
        device_uuid: _Optional[str] = ...,
        device_token: _Optional[str] = ...,
        tx_id: _Optional[str] = ...,
        mode: _Optional[str] = ...,
        items: _Optional[_Iterable[str]] = ...,
        attributes: _Optional[_Union[AuthenticationRequest.Attributes, _Mapping]] = ...,
    ) -> None: ...

class AuthenticationCheckRequest(_message.Message):
    __slots__ = ("tx_id", "attempts")
    TX_ID_FIELD_NUMBER: _ClassVar[int]
    ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    tx_id: str
    attempts: int
    def __init__(self, tx_id: _Optional[str] = ..., attempts: _Optional[int] = ...) -> None: ...

class AuthenticationResponse(_message.Message):
    __slots__ = ("status", "decided_item")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DECIDED_ITEM_FIELD_NUMBER: _ClassVar[int]
    status: AuthenticationResponseStatus
    decided_item: str
    def __init__(
        self, status: _Optional[_Union[AuthenticationResponseStatus, str]] = ..., decided_item: _Optional[str] = ...
    ) -> None: ...
