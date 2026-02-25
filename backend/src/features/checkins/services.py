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


async def get_daily_checkin(senior_id: UUID, session) -> CheckIn:
    senior = None
    if not senior:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Couldn't find senior {senior_id}")
    return None


async def get_missing_checkin_history(senior_id: UUID, session) -> list:
    senior = None
    if not senior:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Couldn't find senior {senior_id}")
    return []


async def get_check_in_history(senior_id: UUID, session) -> list:
    senior = None
    if not senior:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Couldn't find senior {senior_id}")
    return []


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