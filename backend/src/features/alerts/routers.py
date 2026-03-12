from uuid import UUID

from core.database.session import get_session
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from features.checkins.models import CheckIn
from features.relationships.models import Relationship
from features.users.models import User
from shared.api_response import ApiResponse
from sqlmodel import Session, select

from features.alerts.models import Alert


def _get_user_by_email(email: str, session: Session) -> User:
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticated user not found",
        )
    return user

router = APIRouter()

@router.patch("/{alert_id}/resolve", response_model=ApiResponse[Alert])
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

    #Filter table alerts with the id passed in the path parameter 
    alert = db.exec(select(Alert).where(Alert.id == alert_id)).first()

    if not alert:
        raise HTTPException(404, detail="Alert not found")
    
    #Get the senior id connected to the alert
    senior_referred_by_alert =db.exec(select(CheckIn.senior_id).where(CheckIn.id == alert.checkin_id)).first()

    if not senior_referred_by_alert:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No checkins found"
        )

    #Take all the seniors related to the current user
    seniors_related_to_caregiver=db.exec(
        select(Relationship.senior_id).where(Relationship.caregiver_id == user_id)
        ).all()

    if not seniors_related_to_caregiver:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Relationship not found"
        )

    #Check if the senior id connected to the alert has a relationship with the caregiver
    if senior_referred_by_alert in seniors_related_to_caregiver:
        alert.resolved = True
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return ApiResponse(success=True, message="", data=alert)
    
    raise HTTPException(403, "Not authorized")
