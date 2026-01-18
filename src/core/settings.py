from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.app_env_config import AppEnvConfig
from enums import LogFormat, LogLevel

_app_env_config = AppEnvConfig()


class Settings(BaseSettings):
    app_env: str = _app_env_config.app_env
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
            f".env.{_app_env_config.app_env}",
            f".env.{_app_env_config.app_env}.local",  # gitignored
        ),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
