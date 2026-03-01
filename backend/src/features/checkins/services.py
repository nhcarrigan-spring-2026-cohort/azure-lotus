from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlmodel import Session, select

from features.checkins.models import CheckIn
from features.relationships.models import Relationship
from features.users.models import User
from shared.email_service import send_email_to_missing_checkin
from shared.enums import CheckInStatus
from shared.logging import logger


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


def create_daily_checkins_service(session: Session):
    """Create daily check-ins for seniors that don't already have one today."""
    seniors = session.exec(
        select(User).join(Relationship, User.id == Relationship.senior_id)
    ).all()

    today = datetime.now(timezone.utc).date()

    for senior in seniors:
        existing = session.exec(
            select(CheckIn).where(CheckIn.senior_id == senior.id)
        ).all()

        if any(checkin.created_at.date() == today for checkin in existing):
            continue

        session.add(
            CheckIn(
                senior_id=senior.id,
                created_at=datetime.now(timezone.utc),
                status=CheckInStatus.PENDING,
            )
        )

    try:
        session.commit()
    except Exception as error:
        logger.error("Error creating daily check-ins: %s", error)
        session.rollback()


def mark_missing_and_notify(session: Session):
    """Mark pending check-ins as missed and email caregivers."""
    pending_checkins = session.exec(
        select(CheckIn).where(CheckIn.status == CheckInStatus.PENDING)
    ).all()

    for checkin in pending_checkins:
        caregivers = session.exec(
            select(User)
            .join(Relationship, User.id == Relationship.caregiver_id)
            .where(Relationship.senior_id == checkin.senior_id)
        ).all()

        for caregiver in caregivers:
            send_email_to_missing_checkin(caregiver.email)

        checkin.status = CheckInStatus.MISSED

    try:
        session.commit()
    except Exception as error:
        logger.error("Error marking missing check-ins: %s", error)
        session.rollback()


async def complete_checkin(
    checkin_id: UUID,
    current_user_email: str,
    session: Session,
) -> CheckIn:
    """Mark a check-in as completed and record completed_at.

    Only the senior who owns the check-in may complete it.
    Returns 200 with updated check-in, 403 if not owner, 404 if not found.
    """
    user = _get_user_by_email(current_user_email, session)

    checkin = session.get(CheckIn, checkin_id)
    if not checkin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Check-in {checkin_id} not found",
        )

    if checkin.senior_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not own this check-in",
        )

    checkin.status = "completed"
    checkin.completed_at = datetime.now(timezone.utc)
    session.add(checkin)
    session.commit()
    session.refresh(checkin)
    return checkin

