from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Job Hunt Backend"
    # Example: API_KEY_FOR_EXTERNAL_SERVICE: str | None = None

    # For loading from .env file (optional, but good practice)
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')

settings = Settings() 