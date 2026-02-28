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
    VERSION: str = "0.1.0"
    ENV: str = os.getenv("ENV", "development")

    # Security
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "unsafe-secret")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
    ALGORITHM: str = "HS256"

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    DATABASE_TEST_URL: str = os.getenv("DATABASE_TEST_URL")

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = os.getenv("BACKEND_CORS_ORIGINS", "").split(",")

    # EMAIL / SMTP (MailHog)
    NO_REPLY_EMAIL: str = os.getenv("NO_REPLY_EMAIL", "noreply@azure-lotus.local")
    SMTP_HOST: str = os.getenv("SMTP_HOST", "mailhog")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "1025"))
    SMTP_FROM_EMAIL: str = os.getenv("SMTP_FROM_EMAIL", "noreply@azure-lotus.local")


settings = Settings()
