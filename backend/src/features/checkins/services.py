from fastapi import HTTPException, status
from uuid import UUID

from .models import CheckIn


async def get_daily_checkin(senior_id: UUID, session) -> CheckIn:
    """Get the daily check-in for a senior.
    
    This will notify all caregivers associated with this senior through their relationships.
    """
    # TODO: Verify senior exists by checking users table
    senior = None
    if not senior:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Couldn't find senior {senior_id}",
        )
        
    # TODO: Query checkins by senior_id for today
    daily_checkin = None
    return daily_checkin
    
async def get_missing_checkin_history(senior_id: UUID, session) -> CheckIn:
    """Get the missing check-in history for a senior."""
    # TODO: Verify senior exists
    senior = None
    if not senior:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Couldn't find senior {senior_id}",
        )

    # TODO: Query for missed check-ins
    missing_checkin_history = []
    return missing_checkin_history

async def get_check_in_history(senior_id: UUID, session) -> CheckIn:
    """Get the check-in history for a senior."""
    # TODO: Verify senior exists
    senior = None
    if not senior:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Couldn't find senior {senior_id}",
        )
    
    # TODO: Query all check-ins for this senior
    checkin_history = []
    return checkin_history


async def trigger_alert(
    checkin_id: UUID,
    current_user_email: str,
    session,
) -> CheckIn:
    """Set a check-in to ALERTED status and create alert records for all caregivers.

    - 404 if check-in not found
    - 403 if senior does not own the check-in
    - 400 if already ALERTED
    - Creates one Alert record per caregiver relationship with the senior.
    """
    from datetime import datetime, timezone

    from sqlmodel import select

    from features.alerts.models import Alert
    from features.relationships.models import Relationship
    from features.users.models import User

    user = session.exec(select(User).where(User.email == current_user_email)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticated user not found",
        )

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

    if checkin.status == "alerted":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This check-in has already been alerted",
        )

    checkin.status = "alerted"
    session.add(checkin)
    session.flush()

    # Create one Alert record — notifies all caregivers via the relationship table
    relationships = session.exec(
        select(Relationship).where(Relationship.senior_id == checkin.senior_id)
    ).all()

    for rel in relationships:
        alert = Alert(
            checkin_id=checkin.id,
            alert_type="emergency",
            resolved=False,
        )
        session.add(alert)

    # If no relationships exist, still create one alert
    if not relationships:
        session.add(Alert(checkin_id=checkin.id, alert_type="emergency", resolved=False))

    session.commit()
    session.refresh(checkin)
    return checkin