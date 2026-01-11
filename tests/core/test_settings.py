from core.settings import Settings


def test_settings_default_values():
    settings = Settings()

    assert settings.log_level.name == "INFO"
    assert settings.db_url == "sqlite:///data/database.db"
    assert settings.redis_url == "redis://localhost:6379"
