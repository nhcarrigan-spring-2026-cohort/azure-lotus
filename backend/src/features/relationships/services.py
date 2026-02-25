from uuid import UUID

from fastapi import HTTPException, status
from sqlmodel import Session, select

from features.checkins.models import CheckIn
from features.relationships.models import Relationship
from features.users.models import User


async def get_checkin_history(
    relationship_id: UUID,
    current_user_email: str,
    session: Session,
    page: int,
    limit: int,
) -> dict:
    """Return paginated check-in history for the senior in a relationship.

    Validates that the requesting user is either the senior or a caregiver
    named in the relationship before returning data.
    """
    # Look up the relationship
    relationship = session.get(Relationship, relationship_id)
    if not relationship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Relationship {relationship_id} not found",
        )

    # Resolve the requesting user from their email
    current_user = session.exec(
        select(User).where(User.email == current_user_email)
    ).first()
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticated user not found",
        )

    # Ownership check: user must be the senior or the caregiver in this relationship
    if current_user.id not in (relationship.senior_id, relationship.caregiver_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this relationship",
        )

    # Paginate check-ins for this senior, newest first
    offset = (page - 1) * limit
    checkins = session.exec(
        select(CheckIn)
        .where(CheckIn.senior_id == relationship.senior_id)
        .order_by(CheckIn.created_at.desc())
        .offset(offset)
        .limit(limit)
    ).all()

    # Total count for pagination metadata
    total = session.exec(
        select(CheckIn).where(CheckIn.senior_id == relationship.senior_id)
    ).all()

    return {
        "items": checkins,
        "page": page,
        "limit": limit,
        "total": len(total),
    }
