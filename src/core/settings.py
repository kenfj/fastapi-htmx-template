from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.app_env_config import AppEnvConfig
from enums import LogFormat, LogLevel
from enums.app_env import AppEnv  # noqa: TC001

_app_env_config = AppEnvConfig()
_APP_ENV = _app_env_config.app_env


class Settings(BaseSettings):
    app_env: AppEnv = _APP_ENV
    log_level: LogLevel = LogLevel.INFO
    log_format: LogFormat = LogFormat.TEXT
    db_url: str = Field(default=...)
    db_echo: bool = Field(default=False)
    redis_url: str = Field(default=...)

    model_config = SettingsConfigDict(
        env_prefix="app_",
        env_file=(
            ".env",
            ".env.local",  # gitignored
            f".env.{_APP_ENV}",
            f".env.{_APP_ENV}.local",  # gitignored
        ),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
