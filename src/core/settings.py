from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.app_env_config import APP_ENV
from enums.log_level import LogLevel


class Settings(BaseSettings):
    log_level: LogLevel = LogLevel.INFO
    db_url: str = Field(default=...)
    redis_url: str = Field(default=...)

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=(
            ".env",
            ".env.local",  # gitignored
            f".env.{APP_ENV}",
            f".env.{APP_ENV}.local",  # gitignored
        ),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
