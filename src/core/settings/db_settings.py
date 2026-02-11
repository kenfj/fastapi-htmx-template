from pydantic import Field

from core.settings.common_settings import CommonSettings


class DatabaseSettings(CommonSettings):
    db_host: str = Field(default="127.0.0.1")
    db_port: int = Field(default=5432)
    db_name: str = Field(default=...)
    db_user: str = Field(default=...)
    db_password: str = Field(default=...)
    db_schema: str = Field(default=...)
    db_echo: bool = Field(default=False)

    @property
    def db_url(self) -> str:
        return f"postgresql+psycopg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


db_settings = DatabaseSettings()
