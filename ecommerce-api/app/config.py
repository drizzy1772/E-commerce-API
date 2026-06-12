




from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    APP_NAME: str = "E-commerce API"
    DEBUG: bool = False
    model_config = SettingsConfigDict(env_file=".env")
    
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    RESEND_API_KEY: str
    SECRET_KEY: str
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
settings = Settings()