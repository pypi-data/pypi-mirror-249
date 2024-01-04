import dataclasses
import attr

from lark_oapi.remaintain.extra import ACCESS_TOKEN_TYPE_TENANT
from lark_oapi.remaintain.extra.api import set_timeout, Request
from lark_oapi.remaintain.shortcut.compact import FeishuOpenAPICompactSettings


@attr.s
class Message:
    message_id = attr.ib(type=str)


class FeishuMessageShortcutOperationError(Exception):
    pass


@dataclasses.dataclass
class FeishuMessageShortcut:
    s: FeishuOpenAPICompactSettings

    def __post_init__(self):
        pass

    def send_group_robot_message(self, body) -> str:
        conf = self.s.remaintain_extra_config
        req = Request(
            "/open-apis/message/v4/send",
            "POST",
            ACCESS_TOKEN_TYPE_TENANT,
            body,
            output_class=Message,
            request_opts=[set_timeout(3)],
        )
        resp = req.do(conf)
        # print("header = %s" % resp.get_header().items())
        # print("request id = %s" % resp.get_request_id())
        # print(resp)
        if resp.code != 0:
            raise FeishuMessageShortcutOperationError(f"{resp.msg}({resp.error})")
        return resp.data.message_id
