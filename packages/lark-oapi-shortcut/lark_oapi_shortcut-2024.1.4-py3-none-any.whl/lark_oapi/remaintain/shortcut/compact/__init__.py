import dataclasses
from typing import Optional

import urllib3

from lark_oapi import Client
from lark_oapi.remaintain import extra
from lark_oapi.remaintain.extra import DOMAIN_FEISHU, LEVEL_ERROR

DEFAULT_RETRY_CONFIG = urllib3.Retry(
    total=3,
    backoff_factor=0.1,
    status_forcelist=frozenset([413, 429, 502, 503, 504]),
)


@dataclasses.dataclass(repr=False)
class FeishuOpenAPICompactSettings:
    app_id: str
    app_secret: str
    name: str = "Feishu OAPI App"
    log_level: int = LEVEL_ERROR
    requests_retry_config: Optional[urllib3.Retry] = None

    # post init
    remaintain_extra_app_settings: extra.AppSettings = dataclasses.field(init=False)
    remaintain_extra_config: extra.Config = dataclasses.field(init=False)
    upstream_client: Client = dataclasses.field(init=False)

    def __post_init__(self):
        app_settings = extra.Config.new_internal_app_settings(
            app_id=self.app_id,
            app_secret=self.app_secret,
        )
        self.remaintain_extra_app_settings = app_settings
        requests_retry_config = self.requests_retry_config
        self.remaintain_extra_config = extra.Config(
            DOMAIN_FEISHU,
            app_settings,
            log_level=self.log_level,
            requests_retry_config=requests_retry_config,
        )
        self.upstream_client = (
            Client.builder()
            .app_id(
                self.app_id,
            )
            .app_secret(
                self.app_secret,
            )
            .requests_retry_config(requests_retry_config)
            .build()
        )
