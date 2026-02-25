from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlmodel import Session, select

from features.checkins.models import CheckIn
from features.relationships.models import Relationship
from features.users.models import User


async def _resolve_relationship_and_user(
    relationship_id: UUID,
    current_user_email: str,
    session: Session,
) -> tuple[Relationship, User]:
    """Shared helper: fetch relationship + requesting user and enforce ownership."""
    relationship = session.get(Relationship, relationship_id)
    if not relationship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Relationship {relationship_id} not found",
        )

    current_user = session.exec(
        select(User).where(User.email == current_user_email)
    ).first()
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticated user not found",
        )

    if current_user.id not in (relationship.senior_id, relationship.caregiver_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this relationship",
        )

    return relationship, current_user


async def get_checkin_history(
    relationship_id: UUID,
    current_user_email: str,
    session: Session,
    page: int,
    limit: int,
) -> dict:
    """Return paginated check-in history for the senior in a relationship."""
    relationship, _ = await _resolve_relationship_and_user(
        relationship_id, current_user_email, session
    )

    offset = (page - 1) * limit
    checkins = session.exec(
        select(CheckIn)
        .where(CheckIn.senior_id == relationship.senior_id)
        .order_by(CheckIn.created_at.desc())
        .offset(offset)
        .limit(limit)
    ).all()

    total = len(
        session.exec(
            select(CheckIn).where(CheckIn.senior_id == relationship.senior_id)
        ).all()
    )

    return {"items": checkins, "page": page, "limit": limit, "total": total}


async def get_missing_checkins(
    relationship_id: UUID,
    current_user_email: str,
    session: Session,
) -> list[CheckIn]:
    """Return missed check-ins for the senior in a relationship.

    A check-in is considered missed when:
    - its status is 'missed', OR
    - its status is 'pending' and it was created on a previous day (past deadline).
    Results are ordered newest first.
    """
    relationship, _ = await _resolve_relationship_and_user(
        relationship_id, current_user_email, session
    )

    today = datetime.now(timezone.utc).date()

    all_checkins = session.exec(
        select(CheckIn)
        .where(CheckIn.senior_id == relationship.senior_id)
        .order_by(CheckIn.created_at.desc())
    ).all()

    missed = [
        c
        for c in all_checkins
        if c.status == "missed"
        or (c.status == "pending" and c.created_at.date() < today)
    ]

    return missed


async def create_relationship(
    current_user_email: str,
    target_email: str,
    session: Session,
) -> Relationship:
    """Create a relationship where the requesting user monitors a senior by email.

    Rules:
    - Target user must exist (404).
    - Cannot monitor yourself (409).
    - Relationship must not already exist (409).
    """
    current_user = session.exec(
        select(User).where(User.email == current_user_email)
    ).first()
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticated user not found",
        )

    target_user = session.exec(
        select(User).where(User.email == target_email)
    ).first()
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user found with email {target_email}",
        )

    if current_user.id == target_user.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You cannot create a relationship with yourself",
        )

    existing = session.exec(
        select(Relationship).where(
            Relationship.senior_id == target_user.id,
            Relationship.caregiver_id == current_user.id,
        )
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Relationship already exists",
        )

    relationship = Relationship(
        senior_id=target_user.id,
        caregiver_id=current_user.id,
    )
    session.add(relationship)
    session.commit()
    session.refresh(relationship)
    return relationship


async def delete_relationship(
    relationship_id: UUID,
    current_user_email: str,
    session: Session,
) -> None:
    """Delete a relationship. Only the senior or caregiver may do this.

    Check-in history is not affected (checkins reference the senior directly).
    """
    relationship, _ = await _resolve_relationship_and_user(
        relationship_id, current_user_email, session
    )
    session.delete(relationship)
    session.commit()
