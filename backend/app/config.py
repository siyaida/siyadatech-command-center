from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """KSA-native provider configuration. All secrets via environment variables."""
    
    # Application
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "info"
    
    # Database
    DATABASE_URL: str = "postgresql://ragaban:ragaban@localhost:5432/ragaban"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    
    # Providers — KSA Native
    UNIFONIC_API_KEY: str | None = None
    UNIFONIC_BASE_URL: str = "https://api.unifonic.com"
    
    NPHIES_CLIENT_ID: str | None = None
    NPHIES_CLIENT_SECRET: str | None = None
    NPHIES_BASE_URL: str = "https://nphies.seha.sa"
    NPHIES_TOKEN_URL: str = "https://idp.nphies.sa/oauth2/token"
    
    GEIDEA_API_KEY: str | None = None
    GEIDEA_MERCHANT_ID: str | None = None
    GEIDEA_BASE_URL: str = "https://api.geidea.net"
    
    STC_CLOUD_CREDENTIALS: str | None = None
    
    SDAIA_API_KEY: str | None = None
    SDAIA_BASE_URL: str = "https://marketplace.sdai.gov.sa"
    
    TAWK_PROPERTY_ID: str | None = None
    
    # Security
    SECRET_KEY: str = "change-me-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
