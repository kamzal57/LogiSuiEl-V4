from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings."""
    
    # Application
    app_name: str = "LogiSuiEl School Management"
    app_version: str = "4.0.0"
    debug: bool = True
    
    # Database
    database_url: str = "sqlite+aiosqlite:///./school_management.db"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production-use-openssl-rand-hex-32"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
