from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    PROJECT_NAME: str = "EMS Payroll System"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = "YOUR_SUPER_SECRET_KEY_CHANGE_IN_PROD"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/payroll_db"
    
    # Path for exports and pdfs
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    EXPORTS_DIR: Path = BASE_DIR / "exports"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
