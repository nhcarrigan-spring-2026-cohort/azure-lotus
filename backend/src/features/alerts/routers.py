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


def get_relationships_by_id(user_id: UUID, session: Session):
    relationships = session.exec(
        select(Relationship).where(user_id == Relationship.caregiver_id)
    )
    if not relationships:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Relationship not found"
        )

    return relationships


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

    #Filter table relationships by the caregiver id
    relationships = get_relationships_by_id(user_id, db)

    '''
    for r in relationship:
        print(f'\nROW type:{type(r)}')
        print(f'ROW CONTENT:{r}\n')
    '''

    #Filter table alerts with the id passed in the path parameter 
    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if not alert:
        raise HTTPException(404, detail="Alert not found")

    #Take the checkin_id of such alert
    checkin_id = alert.checkin_id

    #Get the senior id connected to that alert filtering by the checkin_id
    senior_referred_by_alert = get_checkin_by_id(checkin_id, db).senior_id

    # Compare if the senior_id in the relationship is equal to senior_id in the checkin that triggered the alert
    #relationship_senior_id = relationships.senior_id
    for r in relationships:
        if r.senior_id == senior_referred_by_alert:
            alert.resolved = True
            db.add(alert)
            db.commit()
            db.refresh(alert)
            return ApiResponse(success=True, message="", data=alert)

    raise HTTPException(403, "Not authorized")


