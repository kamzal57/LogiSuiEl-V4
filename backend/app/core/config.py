from functools import lru_cache
from typing import List

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class TokensConfig(BaseModel):
    secret_key: str = "change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 24 * 7


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__", env_prefix="LOGISUIEL_")

    debug: bool = False
    app_name: str = "LogiSuiEl API"
    backend_cors_origins: List[str] = ["http://localhost:5173"]
    database_url: str = "sqlite+aiosqlite:///./logisuiel.db"
    tokens: TokensConfig = TokensConfig()

    admin_default_username: str = "admin"
    admin_default_password: str = "admin"
    teacher_default_username: str = "test"
    teacher_default_password: str = "test"


@lru_cache
def get_settings() -> Settings:
    return Settings()
