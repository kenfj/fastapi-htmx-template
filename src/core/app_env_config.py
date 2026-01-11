from pydantic_settings import BaseSettings

from enums import AppEnv


class AppEnvConfig(BaseSettings):
    app_env: AppEnv = AppEnv.development


_app_env_config = AppEnvConfig()
APP_ENV = _app_env_config.app_env
