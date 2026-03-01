from uuid import UUID

from fastapi import HTTPException, status
from sqlmodel import Session, select

from features.alerts.models import Alert
from features.checkins.models import CheckIn
from features.relationships.models import Relationship
from features.users.models import User


async def get_alerts_for_user(current_user_email: str, session: Session) -> list[dict]:
    """Get all unresolved alerts for seniors the current user is a caregiver for."""
    current_user = session.exec(
        select(User).where(User.email == current_user_email)
    ).first()
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticated user not found",
        )

    # Find all seniors this user monitors
    relationships = session.exec(
        select(Relationship).where(Relationship.caregiver_id == current_user.id)
    ).all()

    senior_ids = [r.senior_id for r in relationships]

    if not senior_ids:
        return []

    # Get checkins for those seniors
    checkins = session.exec(
        select(CheckIn).where(CheckIn.senior_id.in_(senior_ids))
    ).all()

    checkin_ids = [c.id for c in checkins]

    if not checkin_ids:
        return []

    # Get unresolved alerts for those checkins
    alerts = session.exec(
        select(Alert).where(
            Alert.checkin_id.in_(checkin_ids),
            Alert.resolved == False,
        )
    ).all()

    result = []
    checkin_map = {c.id: c for c in checkins}
    for alert in alerts:
        checkin = checkin_map.get(alert.checkin_id)
        result.append({
            "id": str(alert.id),
            "checkin_id": str(alert.checkin_id),
            "senior_id": str(checkin.senior_id) if checkin else None,
            "alert_type": alert.alert_type,
            "resolved": alert.resolved,
            "created_at": str(alert.created_at),
        })

    return result


async def resolve_alert(alert_id: UUID, current_user_email: str, session: Session) -> Alert:
    """Mark an alert as resolved."""
    current_user = session.exec(
        select(User).where(User.email == current_user_email)
    ).first()
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticated user not found",
        )

    alert = session.get(Alert, alert_id)
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert {alert_id} not found",
        )

    alert.resolved = True
    session.add(alert)
    session.commit()
    session.refresh(alert)
    return alert
