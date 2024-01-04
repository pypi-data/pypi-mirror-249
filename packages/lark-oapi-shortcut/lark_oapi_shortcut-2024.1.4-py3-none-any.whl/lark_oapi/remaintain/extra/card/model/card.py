from typing import Dict

from ...model.oapi_request import OapiRequest
from ...model.oapi_response import OapiResponse
import attr


@attr.s
class Header:
    time_stamp = attr.ib(type=str, default="")
    nonce = attr.ib(type=str, default="")
    signature = attr.ib(type=str, default="")
    refresh_token = attr.ib(type=str, default="")


@attr.s
class Challenge:
    challenge = attr.ib(type=str, default="")
    token = attr.ib(type=str, default="")
    type = attr.ib(type=str, default="")


@attr.s
class Action:
    value = attr.ib(type=Dict, default="")
    tag = attr.ib(type=str, default="")
    option = attr.ib(type=str, default="")
    timezone = attr.ib(type=str, default="")


@attr.s
class Card:
    open_id = attr.ib(type=str, default="")
    user_id = attr.ib(type=str, default="")
    open_message_id = attr.ib(type=str, default="")
    tenant_key = attr.ib(type=str, default="")
    token = attr.ib(type=str, default="")
    timezone = attr.ib(type=str, default="")
    action = attr.ib(type=Action, default="")


@attr.s
class HTTPCard:
    request = attr.ib(type=OapiRequest, default=None)
    response = attr.ib(type=OapiResponse, default=None)
    challenge = attr.ib(type=str, default="")
    type = attr.ib(type=str, default="")
