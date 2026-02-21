from fastapi import APIRouter, Depends
from sqlmodel import Session

from core.database.session import get_session
from features.checkins.models import CheckIn
from shared.api_response import ApiResponse

from .services import (
    get_check_in_history,
    get_daily_checkin,
    get_missing_checkin_history,
)

router = APIRouter()


@router.get("/{senior_id}/daily", response_model=ApiResponse[CheckIn])
async def senior_daily_checkin(senior_id: int, session: Session = Depends(get_session)):
    """Get the daily check-in of one senior"""
    daily_checkin = await get_daily_checkin(senior_id, session)
    return ApiResponse(success=True, message="", data=daily_checkin)


@router.get("/{senior_id}/history", response_model=ApiResponse[CheckIn])
async def senior_checkin_history(
    senior_id: int, session: Session = Depends(get_session)
):
    """Get the history of check-ins of one senior"""
    checkin_history = await get_check_in_history(senior_id, session)
    return ApiResponse(success=True, message="", data=checkin_history)


@router.get("/{senior_id}/missing", response_model=ApiResponse[CheckIn])
async def senior_missing_checkin_history(
    senior_id: int, session: Session = Depends(get_session)
):
    """Get the missing history of check-ins of one senior"""
    missing_checkin_history = await get_missing_checkin_history(senior_id, session)
    return ApiResponse(success=True, message="", data=missing_checkin_history)
