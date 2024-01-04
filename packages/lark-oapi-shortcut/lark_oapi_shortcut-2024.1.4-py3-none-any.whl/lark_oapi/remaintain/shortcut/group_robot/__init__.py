import dataclasses
import os
import time
from typing import Optional

import requests
import urllib3

import hashlib
import base64
import hmac

from requests.adapters import HTTPAdapter


class FeishuGroupRobotOperationError(Exception):
    pass


@dataclasses.dataclass
class FeishuGroupRobotShortCut:
    """
    doc: https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot
    自定义机器人的频率控制和普通应用不同，为 100 次/分钟，5 次/秒。
    """
    web_hook_url: str
    name: str = "群机器人"
    sign_secret: str = ""
    requests_session: Optional[requests.Session] = None
    requests_retry_config: Optional[urllib3.Retry] = None

    def __post_init__(self):
        if not isinstance(self.requests_session, requests.Session):
            self.requests_session = requests.Session()
        if isinstance(self.requests_retry_config, urllib3.Retry):
            retry_adapter = HTTPAdapter(max_retries=self.requests_retry_config)
            self.requests_session.mount('https://', retry_adapter)
            self.requests_session.mount('http://', retry_adapter)

    @classmethod
    def gen_sign(cls, timestamp: int, secret: str):
        """
        modified from https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot#3c6592d6
        """
        # 拼接timestamp和secret
        string_to_sign = f'{timestamp}\n{secret}'
        hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
        # 对结果进行base64处理
        sign = base64.b64encode(hmac_code).decode('utf-8')
        return sign

    def send_message(self, message_data: dict) -> None:
        data = {}
        data.update(message_data)
        if self.sign_secret:
            ts = int(time.time())
            data.update({
                "timestamp": ts,
                "sign": self.gen_sign(ts, self.sign_secret)
            })
        raw_resp = self.requests_session.post(self.web_hook_url, json=data)
        try:
            resp_data = raw_resp.json()
        except:
            resp_data = {}

        if raw_resp.status_code != 200 or resp_data.get("code") != 0:
            raise FeishuGroupRobotOperationError(f"{resp_data.get('msg')}({resp_data.get('code')})")


def example():
    FeishuGroupRobotShortCut(
        web_hook_url=os.environ.get("LARK_OAPI_GROUP_ROBOT_SHORTCUT_WEB_HOOK_URL", ""),
        sign_secret=os.environ.get("LARK_OAPI_GROUP_ROBOT_SHORTCUT_SIGN_SECRET", ""),
    ).send_message(
        message_data={
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": "项目更新通知",
                        "content": [
                            [{
                                "tag": "text",
                                "text": "项目有更新: "
                            },
                                {
                                    "tag": "a",
                                    "text": "请查看",
                                    "href": "http://www.example.com/"
                                },
                                {
                                    "tag": "at",
                                    "user_id": "ou_18eac8********17ad4f02e8bbbb"
                                }
                            ]
                        ]
                    }
                }
            }
        },
    )
