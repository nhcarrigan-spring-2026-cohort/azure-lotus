from fastapi import HTTPException, status
from uuid import UUID

from .models import CheckIn


async def get_daily_checkin(relationship_id: UUID, session) -> CheckIn:
    relationship = None
    if not relationship:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Couldn't find relationship {relationship_id}",
        )
        
    daily_checkin = None
    return daily_checkin
    
async def get_missing_checkin_history(relationship_id: UUID, session) -> CheckIn:
    relationship = None
    if not relationship:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Couldn't find relationship {relationship_id}",
        )

    missing_checkin_history = []
    return missing_checkin_history

async def get_check_in_history(relationship_id: UUID, session) -> CheckIn:
    relationship = None
    if not relationship:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Couldn't find relationship {relationship_id}",
        )
    
    checkin_history = []
    return checkin_history 