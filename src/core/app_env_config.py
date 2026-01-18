from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from enums import AppEnv  # noqa: TC001


class AppEnvConfig(BaseSettings):
    app_env: AppEnv = Field(default=...)

    model_config = SettingsConfigDict(env_file=(".env", ".env.local"))
