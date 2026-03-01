from uuid import UUID

from fastapi import APIRouter, Depends, Request
from sqlmodel import Session

from core.database.session import get_session
from features.checkins.models import CheckIn, CheckInWithSenior
from shared.api_response import ApiResponse

from .services import (
    get_caregiver_dashboard,
    get_check_in_history,
    get_daily_checkin,
    get_missing_checkin_history,
)

router = APIRouter()


@router.get("/dashboard", response_model=ApiResponse[list[CheckInWithSenior]])
async def caregiver_dashboard(request: Request, session: Session = Depends(get_session)):
    """Return caregiver dashboard rows using authenticated user identity."""
    current_user_email: str = request.state.current_user["email"]
    data = await get_caregiver_dashboard(
        current_user_email=current_user_email,
        session=session,
    )
    return ApiResponse(success=True, message="Dashboard data retrieved", data=data)


@router.get("/{senior_id}/daily", response_model=ApiResponse[CheckIn])
async def senior_daily_checkin(
    senior_id: UUID,
    session: Session = Depends(get_session),
):
    """Get the daily check-in of a senior."""
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
