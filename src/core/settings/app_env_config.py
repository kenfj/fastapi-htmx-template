from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from enums import AppEnv  # noqa: TC001


class _AppEnvConfig(BaseSettings):
    app_env: AppEnv = Field(default=...)

    model_config = SettingsConfigDict(
        env_file=(
            ".env",
            ".env.local",
        ),
        env_file_encoding="utf-8",
        extra="ignore",
    )


app_env_config = _AppEnvConfig()
