from fastapi import HTTPException, status

from .models import CheckIn


async def get_daily_checkin(senior_id: int, session) -> CheckIn:
    senior = None 
    if not senior:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Couldn't find senior {senior_id}")
        
    daily_checkin = None
    return daily_checkin
    
async def get_missing_checkin_history(senior_id: int, session) -> CheckIn:
    senior = None 
    if not senior:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Couldn't find senior {senior_id}")

    missing_checkin_history = []
    return missing_checkin_history

async def get_check_in_history(senior_id: int, session) -> CheckIn:
    senior = None 
    if not senior:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Couldn't find senior {senior_id}")
    
    checkin_history = []
    return checkin_history 