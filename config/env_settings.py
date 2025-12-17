"""
Pydantic settings для переменных окружения
"""
from pydantic_settings import BaseSettings
from typing import List


class EnvSettings(BaseSettings):
    """Настройки из переменных окружения"""
    
    SECRET_KEY: str  # Обязательное поле, должно быть в .env
    DEBUG: bool = True
    ALLOWED_HOSTS: str = ""
    
    # Database settings
    DB_NAME: str = "customauth"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    
    # JWT settings
    JWT_SECRET_KEY: str  # Обязательное поле, должно быть в .env
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Создаем экземпляр настроек
env_settings = EnvSettings()

