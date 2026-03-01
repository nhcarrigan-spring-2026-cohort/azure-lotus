from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlmodel import Session, select

from features.checkins.models import CheckIn
from features.users.models import User


def _get_user_by_email(email: str, session: Session) -> User:
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticated user not found",
        )
    return user


async def create_todays_checkin(current_user_email: str, session: Session) -> CheckIn:
    """Create today's check-in for the authenticated senior.

    Returns 400 if a check-in already exists for today.
    """
    user = _get_user_by_email(current_user_email, session)
    today = datetime.now(timezone.utc).date()

    existing = session.exec(
        select(CheckIn).where(CheckIn.senior_id == user.id)
    ).all()
    for c in existing:
        if c.created_at.date() == today:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A check-in already exists for today",
            )

    checkin = CheckIn(senior_id=user.id, status="pending")
    session.add(checkin)
    session.commit()
    session.refresh(checkin)
    return checkin


async def get_todays_checkin(
    current_user_email: str, session: Session
) -> Optional[CheckIn]:
    """Return today's check-in for the authenticated senior, or None if it doesn't exist."""
    user = _get_user_by_email(current_user_email, session)
    today = datetime.now(timezone.utc).date()

    checkins = session.exec(
        select(CheckIn).where(CheckIn.senior_id == user.id)
    ).all()

    for c in checkins:
        if c.created_at.date() == today:
            return c
    return None


async def get_daily_checkin(senior_id: UUID, session) -> CheckIn:
    """Get the daily check-in for a senior."""
    senior = None
    if not senior:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Couldn't find senior {senior_id}",
        )
    return None


async def get_missing_checkin_history(senior_id: UUID, session) -> list:
    """Get the missing check-in history for a senior."""
    senior = None
    if not senior:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Couldn't find senior {senior_id}",
        )
    return []


async def get_check_in_history(senior_id: UUID, session) -> list:
    """Get the check-in history for a senior."""
    senior = None
    if not senior:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Couldn't find senior {senior_id}",
        )
    return []