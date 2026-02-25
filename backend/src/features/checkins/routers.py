from fastapi import APIRouter, Depends, Request, status
from sqlmodel import Session
from uuid import UUID

from core.database.session import get_session
from features.checkins.models import CheckIn
from shared.api_response import ApiResponse

from .services import (create_todays_checkin, get_check_in_history,
                       get_daily_checkin, get_missing_checkin_history,
                       get_todays_checkin)

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ApiResponse[CheckIn])
async def create_checkin(request: Request, session: Session = Depends(get_session)):
    """Create today's check-in for the authenticated senior.

    Returns 400 if a check-in already exists for today.
    """
    current_user_email: str = request.state.current_user["email"]
    checkin = await create_todays_checkin(
        current_user_email=current_user_email, session=session
    )
    return ApiResponse(success=True, message="Check-in created", data=checkin)


@router.get("/today", response_model=ApiResponse[CheckIn])
async def today_checkin(request: Request, session: Session = Depends(get_session)):
    """Return today's check-in for the authenticated senior.

    Returns null in the data field (not 404) when no check-in exists yet.
    """
    current_user_email: str = request.state.current_user["email"]
    checkin = await get_todays_checkin(
        current_user_email=current_user_email, session=session
    )
    return ApiResponse(success=True, message="Today's check-in retrieved", data=checkin)


@router.get("/{senior_id}/daily", response_model=ApiResponse[CheckIn])
async def senior_daily_checkin(senior_id: UUID, session: Session = Depends(get_session)):
    """ Get the daily check-in of a senior """
    daily_checkin = await get_daily_checkin(senior_id, session)
    return ApiResponse(success=True, message="", data=daily_checkin)

@router.get("/{senior_id}/history", response_model=ApiResponse[CheckIn])
async def senior_checkin_history(senior_id: UUID, session: Session = Depends(get_session)):
    """ Get the history of check-ins for a senior """
    checkin_history = await get_check_in_history(senior_id, session)
    return ApiResponse(success=True, message="", data=checkin_history)

@router.get("/{senior_id}/missing", response_model=ApiResponse[CheckIn])
async def senior_missing_checkin_history(senior_id: UUID, session: Session = Depends(get_session)):
    """ Get the missing history of check-ins for a senior """
    missing_checkin_history = await get_missing_checkin_history(senior_id, session)
    return ApiResponse(success=True, message="", data=missing_checkin_history)
