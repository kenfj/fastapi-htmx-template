from enum import StrEnum, auto


class AppEnv(StrEnum):
    DEVELOPMENT = auto()
    """local development environment"""
    TEST = auto()
    """CI/CD test environment"""
    STAGING = auto()
    """production-like staging environment"""
    PRODUCTION = auto()
    """production environment"""
