import os
from typing import Tuple, Optional

from urllib3 import Retry

from .consts import APP_TYPE_ISV, APP_TYPE_INTERNAL
from .logger import Logger, LoggerProxy, LEVEL_ERROR, DefaultLogger
from .app_settings import AppSettings
from .store import MemoryStore, Store


class Config:
    def __init__(
        self,
        domain: str,
        app_settings: AppSettings,
        logger: Logger = DefaultLogger(),
        log_level: int = LEVEL_ERROR,
        store: Store = MemoryStore(),
        requests_retry_config: Optional[Retry] = None,
    ):
        self.domain = domain
        self.app_settings = app_settings
        self.logger = LoggerProxy(log_level, logger)
        self.store = store
        self.helpDeskAuthorization = app_settings.get_help_desk_authorization()
        self.requests_retry_config = requests_retry_config

    @staticmethod
    def new_config_with_memory_store(
        domain: str,
        settings: AppSettings,
        logger: Logger,
        log_level: int,
        retry_settings: Optional[Retry] = None,
    ):
        return Config(
            domain,
            settings,
            logger,
            log_level,
            MemoryStore(),
            retry_settings,
        )

    @staticmethod
    def new_config(
        domain: str,
        settings: AppSettings,
        logger: Logger,
        log_level: int,
        store: Store,
        retry_settings: Optional[Retry] = None,
    ):
        return Config(
            domain,
            settings,
            logger,
            log_level,
            store,
            retry_settings,
        )

    @staticmethod
    def __app_settings_from_env() -> Tuple[str, str, str, str, str, str]:
        """
        This function reads app_id, app_secret, ... from system env.
        If app_id or app_secret doesn't exist in system env, a RuntimeError will be raised.
        """

        app_id = os.getenv("APP_ID", "")
        app_secret = os.getenv("APP_SECRET", "")

        verification_token = os.getenv("VERIFICATION_TOKEN", "")
        encrypt_key = os.getenv("ENCRYPT_KEY", "")

        help_desk_id = os.getenv("HELP_DESK_ID", "")
        help_desk_token = os.getenv("HELP_DESK_TOKEN", "")

        if app_id == "":
            raise RuntimeError("environment variables not exist `APP_ID`")
        if app_secret == "":
            raise RuntimeError("environment variables not exist `APP_SECRET`")

        return (
            app_id,
            app_secret,
            verification_token,
            encrypt_key,
            help_desk_id,
            help_desk_token,
        )

    @staticmethod
    def new_isv_app_settings_from_env():
        """
        This static method initialize a new ISV App Settings and read app_id, app_secret, ... from system env
        """

        (
            app_id,
            app_secret,
            verification_token,
            encrypt_key,
            help_desk_id,
            help_desk_token,
        ) = Config.__app_settings_from_env()
        return AppSettings(
            APP_TYPE_ISV,
            app_id,
            app_secret,
            verification_token,
            encrypt_key,
            help_desk_id,
            help_desk_token,
        )

    @staticmethod
    def new_internal_app_settings_from_env():
        """
        This static method initialize a new internal App Settings and read app_id, app_secret, ... from system env
        """

        (
            app_id,
            app_secret,
            verification_token,
            encrypt_key,
            help_desk_id,
            help_desk_token,
        ) = Config.__app_settings_from_env()
        return AppSettings(
            APP_TYPE_INTERNAL,
            app_id,
            app_secret,
            verification_token,
            encrypt_key,
            help_desk_id,
            help_desk_token,
        )

    @staticmethod
    def new_internal_app_settings(
        app_id: str = "",
        app_secret: str = "",
        verification_token: str = "",
        encrypt_key: str = "",
        help_desk_id: str = "",
        help_desk_token: str = "",
    ) -> AppSettings:
        return AppSettings(
            APP_TYPE_INTERNAL,
            app_id,
            app_secret,
            verification_token,
            encrypt_key,
            help_desk_id,
            help_desk_token,
        )

    @staticmethod
    def new_isv_app_settings(
        app_id: str = "",
        app_secret: str = "",
        verification_token: str = "",
        encrypt_key: str = "",
        help_desk_id: str = "",
        help_desk_token: str = "",
    ) -> AppSettings:
        return AppSettings(
            APP_TYPE_ISV,
            app_id,
            app_secret,
            verification_token,
            encrypt_key,
            help_desk_id,
            help_desk_token,
        )
