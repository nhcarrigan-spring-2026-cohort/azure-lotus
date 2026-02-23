from fastapi import APIRouter, Depends
from sqlmodel import Session
from uuid import UUID

from core.database.session import get_session
from features.checkins.models import CheckIn
from shared.api_response import ApiResponse

from .services import (get_check_in_history, get_daily_checkin,
                       get_missing_checkin_history)

router = APIRouter()


@router.get("/{relationship_id}/daily", response_model=ApiResponse[CheckIn])
async def relationship_daily_checkin(relationship_id: UUID, session: Session = Depends(get_session)):
    """ Get the daily check-in of one relationship """
    daily_checkin = await get_daily_checkin(relationship_id, session)
    return ApiResponse(success=True, message="", data=daily_checkin)

@router.get("/{relationship_id}/history", response_model=ApiResponse[CheckIn])
async def relationship_checkin_history(relationship_id: UUID, session: Session = Depends(get_session)):
    """ Get the history of check-ins of one relationship """
    checkin_history = await get_check_in_history(relationship_id, session)
    return ApiResponse(success=True, message="", data=checkin_history)

@router.get("/{relationship_id}/missing", response_model=ApiResponse[CheckIn])
async def relationship_missing_checkin_history(relationship_id: UUID, session: Session = Depends(get_session)):
    """ Get the missing history of check-ins of one relationship """
    missing_checkin_history = await get_missing_checkin_history(relationship_id, session)
    return ApiResponse(success=True, message="", data=missing_checkin_history)
