from pydantic_settings import BaseSettings, SettingsConfigDict

from core.settings.app_env_config import app_env_config


class CommonSettings(BaseSettings):
    _APP_ENV = app_env_config.app_env

    model_config = SettingsConfigDict(
        env_file=(
            ".env",
            ".env.local",
            f".env.{_APP_ENV}",
            f".env.{_APP_ENV}.local",
        ),
        env_file_encoding="utf-8",
        extra="ignore",
    )
