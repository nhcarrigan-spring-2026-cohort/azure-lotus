from uuid import UUID

from fastapi import APIRouter, Depends, Request
from sqlmodel import Session

from core.database.session import get_session
from features.checkins.models import CheckIn
from shared.api_response import ApiResponse

from .services import (
    get_check_in_history,
    get_daily_checkin,
    get_missing_checkin_history,
    trigger_alert,
)

router = APIRouter()


@router.get("/{senior_id}/daily", response_model=ApiResponse[CheckIn])
async def senior_daily_checkin(senior_id: UUID, session: Session = Depends(get_session)):
    """Get the daily check-in of a senior."""
    daily_checkin = await get_daily_checkin(senior_id, session)
    return ApiResponse(success=True, message="", data=daily_checkin)


@router.get("/{senior_id}/history", response_model=ApiResponse[CheckIn])
async def senior_checkin_history(senior_id: UUID, session: Session = Depends(get_session)):
    """Get the history of check-ins for a senior."""
    checkin_history = await get_check_in_history(senior_id, session)
    return ApiResponse(success=True, message="", data=checkin_history)


@router.get("/{senior_id}/missing", response_model=ApiResponse[CheckIn])
async def senior_missing_checkin_history(senior_id: UUID, session: Session = Depends(get_session)):
    """Get the missing history of check-ins for a senior."""
    missing_checkin_history = await get_missing_checkin_history(senior_id, session)
    return ApiResponse(success=True, message="", data=missing_checkin_history)


@router.put("/{checkin_id}/alert", response_model=ApiResponse[CheckIn], status_code=200)
async def alert_checkin(
    checkin_id: UUID,
    request: Request,
    session: Session = Depends(get_session),
):
    """Trigger an emergency alert for a check-in.

    Sets the check-in status to ALERTED and creates Alert records for all
    caregivers connected to the senior via their relationships.
    Returns 400 if the check-in is already ALERTED.
    """
    current_user_email = request.state.current_user["email"]
    checkin = await trigger_alert(checkin_id, current_user_email, session)
    return ApiResponse(
        success=True,
        message="Emergency alert triggered for all caregivers",
        data=checkin,
    )
