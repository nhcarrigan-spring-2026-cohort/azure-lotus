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