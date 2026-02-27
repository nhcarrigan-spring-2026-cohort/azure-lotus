from fastapi import APIRouter
from sqlalchemy import text

from core.setting import Settings
from shared.email_service import send_email_to_missing_checkin
from src.core.database.session import engine

router = APIRouter()


@router.get("/")
async def root():
    return {
        "App Name": Settings.APP_NAME,
        "Version": Settings.VERSION,
        "message": "Hello World",
    }


@router.get("/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "detail": str(e)}


@router.get("/email-test")
def email_test():
    send_email_to_missing_checkin("test-senior-id")

    return {"status": "ok", "message": "Email sent (if email service is configured)"}
