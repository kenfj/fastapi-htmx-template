from core.settings.app_env_config import app_env_config
from core.settings.common_settings import CommonSettings
from enums import LogFormat, LogLevel
from enums.app_env import AppEnv  # noqa: TC001


class AppSettings(CommonSettings):
    app_env: AppEnv = app_env_config.app_env
    log_level: LogLevel = LogLevel.INFO
    log_format: LogFormat = LogFormat.TEXT


app_settings = AppSettings()
