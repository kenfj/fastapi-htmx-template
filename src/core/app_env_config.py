from pydantic import Field
from pydantic_settings import BaseSettings

from enums import AppEnv  # noqa: TC001


class AppEnvConfig(BaseSettings):
    app_env: AppEnv = Field(default=...)


_app_env_config = AppEnvConfig()
APP_ENV = _app_env_config.app_env
