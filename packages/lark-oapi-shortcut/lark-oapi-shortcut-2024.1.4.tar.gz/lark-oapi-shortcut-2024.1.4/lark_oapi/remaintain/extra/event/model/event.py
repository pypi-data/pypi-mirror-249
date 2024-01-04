from typing import Any, Union

from ...model.oapi_request import OapiRequest
from ...model.oapi_response import OapiResponse
import attr


@attr.s
class BaseEvent:
    ts = attr.ib(type=str, default="")
    uuid = attr.ib(type=str, default="")
    token = attr.ib(type=str, default="")
    type = attr.ib(type=str, default="")


@attr.s
class BaseEventData:
    app_id = attr.ib(type=str, default="")
    type = attr.ib(type=str, default="")
    tenant_key = attr.ib(type=str, default="")


@attr.s
class Header:
    event_id = attr.ib(type=str, default="")
    event_type = attr.ib(type=str, default="")
    app_id = attr.ib(type=str, default="")
    tenant_key = attr.ib(type=str, default="")
    create_time = attr.ib(type=str, default="")
    token = attr.ib(type=str, default="")


@attr.s
class Fuzzy:
    schema = attr.ib(type=str, default="")
    token = attr.ib(type=str, default="")
    type = attr.ib(type=str, default="")
    challenge = attr.ib(type=str, default="")
    header = attr.ib(type=Header, default=None)
    event = attr.ib(type=BaseEventData, default=None)


@attr.s
class BaseEventV2:
    schema = attr.ib(type=str, default="")
    header = attr.ib(type=Header, default=None)


@attr.s
class HTTPEvent:
    schema = attr.ib(type=str, default="")
    type = attr.ib(type=str, default="")
    event_type = attr.ib(type=str, default="")
    challenge = attr.ib(type=str, default="")
    error = attr.ib(type=Union[None, Exception], default=None)
    request = attr.ib(type=OapiRequest, default=None)
    response = attr.ib(type=OapiResponse, default=None)
    data = attr.ib(type=Union[None, Any], default=None)
