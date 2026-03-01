from datetime import date, datetime, timezone
from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from sqlmodel import Session, select

from features.alerts.models import Alert
from features.checkins.models import CheckIn
from features.relationships.models import Relationship
from features.users.models import User
from shared.enums import CheckInStatus


def _get_user_by_email(email: str, session: Session) -> User:
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Authenticated user not found")
    return user


async def create_todays_checkin(current_user_email: str, session: Session) -> CheckIn:
    """Create today's check-in for the logged-in senior. Returns 400 if already exists today."""
    user = _get_user_by_email(current_user_email, session)
    today = date.today()
    start_of_day = datetime(today.year, today.month, today.day, tzinfo=timezone.utc)

    existing = session.exec(
        select(CheckIn).where(
            CheckIn.senior_id == user.id,
            CheckIn.created_at >= start_of_day,
        )
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Check-in already exists for today")

    checkin = CheckIn(senior_id=user.id, status=CheckInStatus.PENDING)
    session.add(checkin)
    session.commit()
    session.refresh(checkin)
    return checkin


async def get_todays_checkin(current_user_email: str, session: Session) -> Optional[CheckIn]:
    """Get today's check-in for the logged-in senior. Returns None if not found."""
    user = _get_user_by_email(current_user_email, session)
    today = date.today()
    start_of_day = datetime(today.year, today.month, today.day, tzinfo=timezone.utc)

    checkin = session.exec(
        select(CheckIn).where(
            CheckIn.senior_id == user.id,
            CheckIn.created_at >= start_of_day,
        )
    ).first()

    return checkin


async def complete_checkin(checkin_id: UUID, current_user_email: str, session: Session) -> CheckIn:
    """Mark a check-in as complete and record the completed_at timestamp."""
    user = _get_user_by_email(current_user_email, session)

    checkin = session.get(CheckIn, checkin_id)
    if not checkin:
        raise HTTPException(status_code=404, detail="Check-in not found")
    if checkin.senior_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to complete this check-in")

    checkin.status = CheckInStatus.COMPLETED
    checkin.completed_at = datetime.now(timezone.utc)
    session.add(checkin)
    session.commit()
    session.refresh(checkin)
    return checkin


async def trigger_alert(checkin_id: UUID, current_user_email: str, session: Session) -> CheckIn:
    """Set a check-in to ALERTED and create Alert records for all caregivers.

    - 404 if check-in not found
    - 403 if the current user does not own the check-in
    - 400 if already ALERTED
    """
    user = _get_user_by_email(current_user_email, session)

    checkin = session.get(CheckIn, checkin_id)
    if not checkin:
        raise HTTPException(status_code=404, detail="Check-in not found")
    if checkin.senior_id != user.id:
        raise HTTPException(status_code=403, detail="You do not own this check-in")
    if checkin.status == CheckInStatus.ALERTED:
        raise HTTPException(status_code=400, detail="Check-in is already ALERTED")

    checkin.status = CheckInStatus.ALERTED
    session.add(checkin)
    session.flush()

    relationships = session.exec(
        select(Relationship).where(Relationship.senior_id == user.id)
    ).all()

    for _rel in relationships:
        session.add(Alert(checkin_id=checkin.id, alert_type="emergency", resolved=False))

    if not relationships:
        session.add(Alert(checkin_id=checkin.id, alert_type="emergency", resolved=False))

    session.commit()
    session.refresh(checkin)
    return checkin