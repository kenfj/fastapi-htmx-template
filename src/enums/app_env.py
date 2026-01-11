from enum import StrEnum, auto


class AppEnv(StrEnum):
    development = auto()
    """local development environment"""
    test = auto()
    """CI/CD test environment"""
    staging = auto()
    """production-like staging environment"""
    production = auto()
    """production environment"""
