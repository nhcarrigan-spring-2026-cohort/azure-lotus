from fastapi import APIRouter, Depends, Request, status
from sqlmodel import Session
from uuid import UUID

from core.database.session import get_session
from features.checkins.models import CheckIn
from shared.api_response import ApiResponse

from .services import (complete_checkin, get_check_in_history,
                       get_daily_checkin, get_missing_checkin_history)

router = APIRouter()


@router.put("/{checkin_id}/complete", response_model=ApiResponse[CheckIn])
async def complete_senior_checkin(
    checkin_id: UUID,
    request: Request,
    session: Session = Depends(get_session),
):
    """Mark a check-in as completed and record the completed_at timestamp.

    Only the senior who owns the check-in may call this endpoint.
    Returns 200 with updated check-in, 403 if not owner, 404 if not found.
    """
    current_user_email: str = request.state.current_user["email"]
    checkin = await complete_checkin(
        checkin_id=checkin_id,
        current_user_email=current_user_email,
        session=session,
    )
    return ApiResponse(success=True, message="Check-in completed", data=checkin)


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
