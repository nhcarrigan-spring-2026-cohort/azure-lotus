from uuid import UUID

from core.database.session import get_session
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from features.checkins.models import CheckIn
from features.relationships.models import Relationship
from features.users.models import User
from shared.api_response import ApiResponse
from sqlmodel import Session, select

from .models import Alert


def _get_user_by_email(email: str, session: Session) -> User:
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticated user not found",
        )
    return user


def get_relationship_by_id(user_id: UUID, session: Session):
    relationship = session.exec(
        select(Relationship).where(user_id == Relationship.caregiver_id)
    ).first()
    if not relationship:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Relationship not found"
        )

    return relationship


def get_checkin_by_id(checkin_id: UUID, session: Session):
    checkin = session.exec(select(CheckIn).where(checkin_id == CheckIn.id)).first()
    if not checkin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No checkins found"
        )

    return checkin


router = APIRouter()


@router.patch("/{alert_id}/resolve", response_model=ApiResponse)
async def resolve_alert(
    alert_id: UUID, request: Request, db: Session = Depends(get_session)
):
    """
    Mark an alert as resolved(true) only if the caregiver is monitoring the senior linked to this alert.
    Errors:
        Returns 404 if alert not found
        Return 403 if not authorized
    """

    user_email = request.state.current_user["email"]
    user_id = _get_user_by_email(user_email, db).id

    relationship = get_relationship_by_id(user_id, db)
    relationship_senior_id = relationship.senior_id

    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if not alert:
        raise HTTPException(404, detail="Alert not found")

    checkin_id = alert.checkin_id
    checkin_senior_id = get_checkin_by_id(checkin_id, db).senior_id

    # Compare if the senior_id in the relationship is equal to senior_id in the checkin that triggered the alert
    if checkin_senior_id != relationship_senior_id:
        raise HTTPException(403, "Not authorized")

    alert.resolved = True
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return ApiResponse(success=True, message="", data=alert)
