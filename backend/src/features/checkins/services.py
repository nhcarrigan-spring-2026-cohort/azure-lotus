from datetime import date, datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlmodel import select

from core.database.session import get_session
from features.relationships.models import Relationship
from features.users.models import User
from shared.email_service import send_email_to_missing_checkin
from shared.enums import CheckInStatus, UserRole
from shared.logging import logger

from .models import CheckIn


def check_senior_exists(senior_id: UUID, session) -> bool:
    """Check if a senior exists in the database."""
    result = session.execute(select(User).where(User.id == senior_id))
    senior = result.scalar_one_or_none()
    return senior is not None


async def get_daily_checkin(senior_id: UUID, session) -> CheckIn:
    """Get the daily check-in for a senior."""
    if not check_senior_exists(senior_id, session):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Couldn't find senior {senior_id}",
        )

    query = (
        select(CheckIn)
        .where(CheckIn.senior_id == senior_id)
        .where(
            CheckIn.created_at
            >= datetime.now(timezone.utc).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        )
        .where(
            CheckIn.created_at
            < datetime.now(timezone.utc).replace(
                hour=23, minute=59, second=59, microsecond=999999
            )
        )
    )

    daily_checkin = session.execute(query).scalar_one_or_none()
    return daily_checkin


async def get_missing_checkin_history(senior_id: UUID, payload, session) -> list:
    """Get the missing check-in history for a senior."""
    if not check_senior_exists(senior_id, session):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Couldn't find senior {senior_id}",
        )

    query = (
        select(CheckIn)
        .where(CheckIn.senior_id == senior_id)
        .where(CheckIn.status == CheckInStatus.MISSED)
    )

    if payload.from_date or payload.to_date:
        # Parse string dates to date objects
        from_date = payload.from_date
        to_date = payload.to_date

        if isinstance(from_date, str):
            from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
        if isinstance(to_date, str):
            to_date = datetime.strptime(to_date, "%Y-%m-%d").date()

        if from_date is None:
            from_date = datetime.min.date()
        if to_date is None:
            to_date = datetime.now(timezone.utc).date()

        query = query.where(CheckIn.created_at >= from_date).where(
            CheckIn.created_at <= to_date
        )

    query = query.order_by(CheckIn.created_at.desc())

    result = session.execute(query)
    missing_checkin_history = result.scalars().all()
    return missing_checkin_history


async def get_check_in_history(senior_id: UUID, payload, session) -> list:
    """Get the check-in history for a senior."""
    if not check_senior_exists(senior_id, session):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Couldn't find senior {senior_id}",
        )

    if payload.from_date is None and payload.to_date is None:
        query = select(CheckIn).where(CheckIn.senior_id == senior_id)
    else:
        # Parse string dates to date objects
        from_date = payload.from_date
        to_date = payload.to_date

        if isinstance(from_date, str):
            from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
        if isinstance(to_date, str):
            to_date = datetime.strptime(to_date, "%Y-%m-%d").date()

        if from_date is None:
            from_date = datetime.min.date()
        if to_date is None:
            to_date = datetime.now(timezone.utc).date()

        query = (
            select(CheckIn)
            .where(CheckIn.senior_id == senior_id)
            .where(CheckIn.created_at >= from_date)
            .where(CheckIn.created_at <= to_date)
        )

    result = session.execute(query)
    checkin_history = result.scalars().all()
    return checkin_history


def create_daily_checkins_service(session):
    """Create daily check-in records for all seniors."""

    seniors = session.exec(
        select(User).join(Relationship, User.id == Relationship.senior_id)
    ).all()

    for senior in seniors:
        logger.info(f"Creating daily check-in for senior {senior}")
        session.add(
            CheckIn(
                senior_id=senior,
                created_at=datetime.now(timezone.utc),
                status=CheckInStatus.PENDING,
            )
        )
    try:
        session.commit()
    except Exception as e:
        logger.error(f"Error committing session in create_daily_checkins_service: {e}")
        session.rollback()


def mark_missing_and_notify(session):
    """Mark pending check-ins as missed and notify seniors."""
    result = session.execute(
        select(CheckIn)
        .where(
            CheckIn.created_at
            >= datetime.now(timezone.utc).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        )
        .where(
            CheckIn.created_at
            < datetime.now(timezone.utc).replace(
                hour=23, minute=59, second=59, microsecond=999999
            )
        )
        .where(CheckIn.status == CheckInStatus.PENDING)
    )
    pending_checkins = result.scalars().all()
    for checkin in pending_checkins:
        # Send Email
        caregiver = session.exec(
            select(User)
            .join(Relationship, User.id == Relationship.caregiver_id)
            .where(Relationship.senior_id == checkin.senior_id)
        ).all()

        for caregiver in caregiver:
            send_email_to_missing_checkin(caregiver.email)
        # Update status
        checkin.status = CheckInStatus.MISSED
    try:
        session.commit()
    except Exception as e:
        logger.error(f"Error committing session in mark_missing_and_notify: {e}")
        session.rollback()
