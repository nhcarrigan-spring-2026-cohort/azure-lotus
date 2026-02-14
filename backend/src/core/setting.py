import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[3]  # azure-lotus
BACKEND_DIR = PROJECT_ROOT / "backend"

ENV_FILE = BACKEND_DIR / ".env"
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)


class Settings:
    # App
    APP_NAME: str = "Azure Lotus"
    ENV: str = os.getenv("ENV", "development")

    # Security
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "unsafe-secret")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
    ALGORITHM: str = "HS256"

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = os.getenv("BACKEND_CORS_ORIGINS", "").split(",")


settings = Settings()
