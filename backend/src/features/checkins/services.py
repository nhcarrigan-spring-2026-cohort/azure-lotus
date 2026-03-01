from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlmodel import Session, select

from features.relationships.models import Relationship
from features.users.models import User

from .models import CheckIn, CheckInWithSenior


def _get_user_by_email(email: str, session: Session) -> User:
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticated user not found",
        )
    return user


async def get_caregiver_dashboard(
    current_user_email: str,
    session: Session,
) -> list[CheckInWithSenior]:
    """Return caregiver dashboard rows with senior profile and latest check-in."""
    caregiver = _get_user_by_email(current_user_email, session)

    relationships = session.exec(
        select(Relationship).where(Relationship.caregiver_id == caregiver.id)
    ).all()
    if not relationships:
        return []

    senior_ids = [relationship.senior_id for relationship in relationships]
    seniors = session.exec(select(User).where(User.id.in_(senior_ids))).all()
    seniors_by_id = {senior.id: senior for senior in seniors}

    checkins = session.exec(
        select(CheckIn)
        .where(CheckIn.senior_id.in_(senior_ids))
        .order_by(CheckIn.created_at.desc())
    ).all()

    latest_checkin_by_senior: dict[UUID, CheckIn] = {}
    for checkin in checkins:
        if checkin.senior_id not in latest_checkin_by_senior:
            latest_checkin_by_senior[checkin.senior_id] = checkin

    dashboard_data: list[CheckInWithSenior] = []
    for relationship in relationships:
        senior = seniors_by_id.get(relationship.senior_id)
        if not senior:
            continue

        latest_checkin = latest_checkin_by_senior.get(relationship.senior_id)
        dashboard_data.append(
            CheckInWithSenior(
                relationship_id=relationship.id,
                senior_id=senior.id,
                first_name=senior.first_name,
                last_name=senior.last_name,
                phone_number=senior.phone_number,
                status=latest_checkin.status if latest_checkin else None,
                time=latest_checkin.created_at if latest_checkin else None,
            )
        )

    return dashboard_data


async def get_daily_checkin(senior_id: UUID, session) -> CheckIn:
    """Get the daily check-in for a senior.
    
    This will notify all caregivers associated with this senior through their relationships.
    """
    senior = session.exec(select(User).where(User.id == senior_id)).first()
    if not senior:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Couldn't find senior {senior_id}",
        )

    today = datetime.now(timezone.utc).date()
    checkins = session.exec(
        select(CheckIn)
        .where(CheckIn.senior_id == senior_id)
        .order_by(CheckIn.created_at.desc())
    ).all()
    for checkin in checkins:
        if checkin.created_at.date() == today:
            return checkin
    return None
    
async def get_missing_checkin_history(senior_id: UUID, session) -> CheckIn:
    """Get the missing check-in history for a senior."""
    senior = session.exec(select(User).where(User.id == senior_id)).first()
    if not senior:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Couldn't find senior {senior_id}",
        )
    return session.exec(
        select(CheckIn)
        .where(CheckIn.senior_id == senior_id)
        .where(CheckIn.status == "missed")
        .order_by(CheckIn.created_at.desc())
    ).all()

async def get_check_in_history(senior_id: UUID, session) -> CheckIn:
    """Get the check-in history for a senior."""
    senior = session.exec(select(User).where(User.id == senior_id)).first()
    if not senior:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Couldn't find senior {senior_id}",
        )

    return session.exec(
        select(CheckIn)
        .where(CheckIn.senior_id == senior_id)
        .order_by(CheckIn.created_at.desc())
    ).all()